"""AI models for vulnerability detection"""

__all__ = ["CodeBERTVulnerabilityModel"]


def __getattr__(name):
    if name == "CodeBERTVulnerabilityModel":
        from .codebert_model import CodeBERTVulnerabilityModel
        return CodeBERTVulnerabilityModel
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
