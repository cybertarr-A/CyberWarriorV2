# cyberwarrior/ai/ensemble.py
from dataclasses import dataclass
from typing import List, Dict, Any

from openai import models

from cyberwarrior.ai.codebert_model import CodeBERTVulnerabilityModel
from cyberwarrior.ai.devign_model import DevignVulnerabilityModel
from cyberwarrior.ai.unixcoder_model import UnixCoderVulnerabilityModel


@dataclass
class EnsembleResult:
    vulnerable: bool
    ensemble_score: float  # 0.0–1.0
    severity: str          # info|low|medium|high|critical
    votes_vulnerable: int
    total_models: int
    models: List[Dict[str, Any]]


def _normalize_label(label: str) -> str:
    """
    Try to normalize different model label schemes into:
    'vulnerable' or 'clean'.
    """
    l = label.lower()
    # Common "clean" patterns
    if "no_vul" in l or "no-vul" in l or "clean" in l or "safe" in l or "non-vulnerable" in l:
        return "clean"
    if l in {"0", "non-vulnerable", "not-vulnerable"}:
        return "clean"
    # Default to vulnerable if it's clearly about vulnerabilities
    return "vulnerable"


def _severity_from_score(score: float) -> str:
    """
    Map 0–1 score into typical severity buckets.
    """
    if score < 0.2:
        return "info"
    if score < 0.4:
        return "low"
    if score < 0.6:
        return "medium"
    if score < 0.8:
        return "high"
    return "critical"


class EnsembleVulnerabilityModel:
    def __init__(self):
        print("[WARN] Offline mode: Only CodeBERT enabled.")
        from cyberwarrior.ai.codebert_model import CodeBERTVulnerabilityModel
        self.codebert = CodeBERTVulnerabilityModel()

        # Disable these for now (no tokenizer files offline)
        self.devign = None
        self.unixcoder = None


    def analyze_snippet(self, code_snippet: str) -> EnsembleResult:
        model_outputs: List[Dict[str, Any]] = []

        models = [self.codebert]
        for model in models:

            out = model.predict(code_snippet)
            out["normalized_label"] = _normalize_label(out["label"])
            model_outputs.append(out)

        total_models = len(model_outputs)
        vuln_scores: List[float] = [
            m["score"] for m in model_outputs if m["normalized_label"] == "vulnerable"
        ]
        votes_vulnerable = len(vuln_scores)

        if votes_vulnerable == 0:
            return EnsembleResult(
                vulnerable=False,
                ensemble_score=0.0,
                severity="info",
                votes_vulnerable=0,
                total_models=total_models,
                models=model_outputs,
            )

        # Ensemble score: average of vulnerable scores * vote ratio
        avg_model_score = sum(vuln_scores) / votes_vulnerable
        vote_ratio = votes_vulnerable / total_models
        ensemble_score = float(avg_model_score * vote_ratio)

        severity = _severity_from_score(ensemble_score)

        return EnsembleResult(
            vulnerable=True,
            ensemble_score=ensemble_score,
            severity=severity,
            votes_vulnerable=votes_vulnerable,
            total_models=total_models,
            models=model_outputs,
        )
