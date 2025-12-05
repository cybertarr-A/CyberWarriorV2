# cyberwarrior/analysis/risk_engine.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any
import os
import requests


NVD_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


LABEL_TO_KEYWORD = {
    # You can extend this mapping as you learn the labels returned by the models
    "sql_injection": "sql injection",
    "xss": "cross-site scripting",
    "path_traversal": "path traversal",
    "rce": "remote code execution",
    "command_injection": "command injection",
    "hardcoded_secret": "hard coded credentials",
}


@dataclass
class CVSSInfo:
    base_score: float
    severity: str
    vector: str
    source_cve: str


def label_to_keyword(label: str) -> str:
    l = label.lower()
    for key, kw in LABEL_TO_KEYWORD.items():
        if key in l:
            return kw
    # Fallback: just search by label text
    return label.replace("_", " ")


def fetch_cvss_for_label(label: str) -> Optional[CVSSInfo]:
    """
    Best-effort CVSS fetch from NVD based on a label/keyword.
    Requires internet & (optionally) an NVD API key in NVD_API_KEY env.
    If anything fails, returns None instead of crashing.
    """
    keyword = label_to_keyword(label)
    params = {
        "keywordSearch": keyword,
        "resultsPerPage": 1,
    }
    api_key = os.getenv("NVD_API_KEY")
    headers = {}
    if api_key:
        headers["apiKey"] = api_key

    try:
        resp = requests.get(NVD_BASE_URL, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        vulns = data.get("vulnerabilities") or []
        if not vulns:
            return None

        cve = vulns[0].get("cve", {})
        cve_id = cve.get("id", "UNKNOWN")

        metrics = cve.get("metrics", {})
        # Try V3.1, then V3.0, then V2
        for metric_key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
            arr = metrics.get(metric_key)
            if arr:
                cvss_data = arr[0].get("cvssData", {})
                score = cvss_data.get("baseScore")
                severity = cvss_data.get("baseSeverity") or "UNKNOWN"
                vector = cvss_data.get("vectorString") or ""
                if score is not None:
                    return CVSSInfo(
                        base_score=float(score),
                        severity=str(severity),
                        vector=str(vector),
                        source_cve=cve_id,
                    )
    except Exception:
        return None

    return None
