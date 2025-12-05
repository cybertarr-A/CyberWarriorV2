# cyberwarrior/analysis/analyzer.py

from dataclasses import asdict, dataclass
from typing import List, Dict, Any

from cyberwarrior.ai.ensemble import EnsembleVulnerabilityModel
from cyberwarrior.ai.hf_patcher import HFCloudPatchGenerator
from cyberwarrior.utils.chunker import chunk_code
from cyberwarrior.analysis.risk_engine import fetch_cvss_for_label


@dataclass
class Finding:
    file_path: str
    snippet: str
    ensemble_score: float
    severity: str
    votes_vulnerable: int
    total_models: int
    model_outputs: List[Dict[str, Any]]
    cvss_score: float | None = None
    cvss_severity: str | None = None
    cvss_vector: str | None = None
    cvss_cve: str | None = None
    patch: Dict[str, Any] | None = None


class Analyzer:
    def __init__(self):
        self.ensemble = EnsembleVulnerabilityModel()
        self.patcher = HFCloudPatchGenerator()  # cloud patcher with fallback

    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        findings: List[Finding] = []

        try:
            with open(file_path, "r", errors="ignore") as f:
                code = f.read()
        except Exception:
            return []

        for snippet in chunk_code(code):
            er = self.ensemble.analyze_snippet(snippet)
            if not er.vulnerable:
                continue

            primary_label = er.models[0]["label"]
            cvss = fetch_cvss_for_label(primary_label)

            patch_info: Dict[str, Any] | None = None

            # Only patch high-risk items for compute/latency reasons
            if er.severity in {"high", "critical"}:
                patch = self.patcher.generate(
                    file_path=file_path,
                    snippet=snippet,
                    severity=er.severity,
                    model_outputs=er.models,
                )

                patch_info = {
                    "patched_snippet": patch.patched_snippet,
                    "patch_diff": (
                        getattr(patch, "patch_diff", getattr(patch, "diff", ""))
                    ),
                    "model_used": (
                        getattr(patch, "model", getattr(patch, "model_used", "unknown"))
                    ),
                    "explanation": patch.explanation,
                    "success": patch.success,
                }

            finding = Finding(
                file_path=file_path,
                snippet=snippet[:400],  # small preview to frontend
                ensemble_score=er.ensemble_score,
                severity=er.severity,
                votes_vulnerable=er.votes_vulnerable,
                total_models=er.total_models,
                model_outputs=er.models,
                cvss_score=cvss.base_score if cvss else None,
                cvss_severity=cvss.severity if cvss else None,
                cvss_vector=cvss.vector if cvss else None,
                cvss_cve=cvss.source_cve if cvss else None,
                patch=patch_info,
            )

            findings.append(finding)

        return [asdict(f) for f in findings]
