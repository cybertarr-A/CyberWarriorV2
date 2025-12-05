"""Code analysis and vulnerability detection"""

__all__ = ["Analyzer"]


def __getattr__(name):
    if name == "Analyzer":
        from .analyzer import Analyzer
        return Analyzer
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
