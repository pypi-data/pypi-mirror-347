import glob
import os
import subprocess

from tqdm import tqdm


def call_zeek(pcap_path: str) -> list[str]:
    """
    Call Zeek to process a pcap file and return the contents of the generated log files.

    :param pcap_path: Path to the pcap file (relative to the mounted volume in the Docker container)
    :return: A list of strings, where each string is the content of a Zeek log file
    """

    subprocess.run(
        [
            "docker", "run", "-v", ".:/data", "zeek/zeek", "sh", "-c",
            f"zeek -C -r /data/{pcap_path} && cp *.log /data"
        ],
    )

    log_files = glob.glob("*.log")

    file_contents = []
    for file_path in tqdm(log_files, desc="Processing log files"):
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents.append(file.read())
        # Remove the log file after reading its contents
        os.remove(file_path)
    return file_contents

