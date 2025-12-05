# api_server.py
from __future__ import annotations

from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from cyberwarrior.repo.github_loader import clone_repo_or_load_path, find_code_files
from cyberwarrior.analysis.analyzer import Analyzer


class ScanRequest(BaseModel):
    target: str  # GitHub URL or local path


app = FastAPI(title="CyberWarriorV2 API", version="0.1")

# Allow local frontend (Vite/React) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/scan")
def scan(request: ScanRequest) -> Dict[str, Any]:
    """
    Run a full scan on a GitHub repo or local directory.
    Returns findings grouped by file.
    """
    target = request.target.strip()
    if not target:
        raise HTTPException(status_code=400, detail="target is required")

    try:
        repo_path = clone_repo_or_load_path(target)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load target: {e}")

    analyzer = Analyzer()
    results: Dict[str, Any] = {}
    severity_counts: Dict[str, int] = {}

    files = list(find_code_files(repo_path))

    for file_path in files:
        file_findings = analyzer.analyze_file(file_path)
        if not file_findings:
            continue

        results[file_path] = file_findings
        for f in file_findings:
            sev = f.get("severity", "unknown")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

    return {
        "target": target,
        "file_count": len(files),
        "finding_file_count": len(results),
        "severity_counts": severity_counts,
        "results": results,
    }
