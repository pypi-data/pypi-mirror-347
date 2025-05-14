from concurrent.futures import ThreadPoolExecutor, as_completed

import loguru

from core.config import Master
from tqdm import tqdm

from core.docker_call.zeek_call import call_zeek
from core.llm.agent_pcap import agent_pcap
from core.llm.old.report_sum import sec_report_writer
from core.scheduler.core.init import global_llm


def invoke(input_pcap_path: str, output_report_path: str, INVOKE_THREADS=20):
    """
    最终的做题函数，根据输入的pcap文件路径处理，并在对应路径输出报告
    :param INVOKE_THREADS:
    :param input_pcap_path: *.pcap
    :param output_report_path: *.md
    :return:
    """
    assert input_pcap_path.endswith(".pcap"), "Input file must be a pcap file"
    assert output_report_path.endswith(".md"), "Output file must be a markdown file"

    zeek_res = call_zeek(input_pcap_path)  # [str...]
    sum_res = []
    with global_llm():

        def process_pcap(pcap_log):
            """
            单个 pcap_log 的处理函数
            """
            try:
                reports_sum = agent_pcap(pcap_log=pcap_log)
                loguru.logger.debug(f"raw reports: {reports_sum}")
                valid_reports = []
                for reports in reports_sum:
                    for report in reports.multi_pcap_analysis:
                        loguru.logger.debug(f"report: {report}")
                        if hasattr(report, "attack_info") and hasattr(report.attack_info, "is_attack"):
                            loguru.logger.debug(f"attack_info: {report.attack_info}")
                            if report.attack_info.is_attack:
                                valid_reports.append(report)
                        else:
                            loguru.logger.warning(f"Invalid report structure: {report}")

                return valid_reports
            except Exception as e:
                loguru.logger.error(f"Error processing {e}")
                return None

        with ThreadPoolExecutor(max_workers=INVOKE_THREADS) as executor:
            future_to_log = {
                executor.submit(process_pcap, pcap_log): pcap_log
                for pcap_log in zeek_res
            }

            with tqdm(desc="总进度", total=len(zeek_res)) as pbar:
                for future in as_completed(future_to_log):
                    pcap_log = future_to_log[future]
                    result = future.result()
                    current_log = pcap_log[:32]

                    if result is not None:
                        sum_res.append(result)

                    # 更新进度条
                    pbar.update(1)
                    pbar.set_postfix(current_log=current_log)
    sum_reports = sec_report_writer(reports=sum_res)
    if "</think>" in sum_reports:
        sum_reports = sum_reports.split("</think>")[-1]
    loguru.logger.info(f"Final report: {sum_reports[:64]}...")
    open(output_report_path, "w", encoding=Master.get("encoding", "utf-8")).write(sum_reports)
