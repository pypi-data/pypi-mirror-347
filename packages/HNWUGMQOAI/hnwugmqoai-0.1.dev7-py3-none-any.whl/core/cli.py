from typing import List

import typer

from core.config import Master

import core.invoke.pcap
from core.invoke.eml import invoke

app = typer.Typer(
    name="某比赛的核心cli",
    no_args_is_help=True,
)


@app.command()
def pcap(
        input_path: str = typer.Argument(..., help="Input file path of .pcap."),
        output_path: str = typer.Argument(..., help="Output report path"),
        api_endpoint: str = typer.Argument("https://www.gptapi.us/v1", help="Openai api endpoint"),
        api_key: str = typer.Argument("sk-gnZfIx337omYX3bd30B1C95a0f1047Ee86CaD8925177AbEa", help="Openai api key"),
        default_model: str = typer.Argument("o1-preview", help="Openai model"),
):
    """
    解析pcap文件，生成报告
    :param default_model:
    :param api_key:
    :param api_endpoint:
    :param input_path: 输入的pcap文件路径
    :param output_path: 输出的报告路径
    :return:
    """
    Master['openai_api_endpoint'] = api_endpoint
    Master['openai_api_key'] = api_key
    Master['default_model'] = default_model
    core.invoke.pcap.invoke(input_pcap_path=input_path, output_report_path=output_path)


@app.command()
def binary(
        input_path: str = typer.Argument(..., help="Input folder of binary."),
        output_path: str = typer.Argument(..., help="Output report path"),
):
    """
    解析二进制文件，生成报告
    :param default_model:
    :param api_key:
    :param api_endpoint:
    :param input_path: 输入的二进制文件路径
    :param output_path: 输出的报告路径
    :return:
    """
    ...


@app.command()
def eml(
        input_path: str = typer.Argument(..., help="Input folder of .eml."),
        output_path: str = typer.Argument(..., help="Output report path"),
):
    """
    解析.eml文件，生成报告
    :param input_path: 输入的.eml文件路径
    :param output_path: 输出的报告路径
    :return:
    """
    invoke(input_eml_folder=input_path, output_report_path=output_path)


def main():
    app()


if __name__ == "__main__":
    main()
