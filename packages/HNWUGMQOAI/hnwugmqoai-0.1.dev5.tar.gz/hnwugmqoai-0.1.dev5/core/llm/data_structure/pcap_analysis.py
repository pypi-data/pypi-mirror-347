from enum import Enum
from typing import Optional

from pydantic import BaseModel


class attack_type(Enum):
    SQL_INJECTION = "SQL_INJECTION"
    XSS = "XSS"
    CSRF = "CSRF"
    SSRF = "SSRF"
    RCE = "RCE"
    DDoS = "DDoS"
    MITM = "MITM"
    PHISHING = "PHISHING"
    SSTI = "SSTI"
    XXE = "XXE"
    INFO_LEAK = "INFO_LEAK"


class attack_info(BaseModel):
    is_attack: bool
    attack_type: Optional[attack_type] = None


class pcap_analysis(BaseModel):
    """
    pcap分析结构
    """
    attack_info: attack_info
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int


class multi_pcap_analysis(BaseModel):
    multi_pcap_analysis: list[pcap_analysis]
