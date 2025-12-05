# cyberwarrior/cli.py
import json
from collections import Counter

from tqdm import tqdm

from cyberwarrior.repo.github_loader import clone_repo_or_load_path, find_code_files
from cyberwarrior.analysis.analyzer import Analyzer


def run_scan(github_url: str, output_file: str):
    repo_path = clone_repo_or_load_path(github_url)
    analyzer = Analyzer()

    results = {}
    severity_counter = Counter()

    files = list(find_code_files(repo_path))
    print(f"[Scan] Total code files found: {len(files)}\n")

    for file in tqdm(files, desc="Analyzing files"):
        findings = analyzer.analyze_file(file)
        if findings:
            results[file] = findings
            for f in findings:
                severity_counter[f.get("severity", "unknown")] += 1

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\n[✔] Scan complete! Results saved to: {output_file}")
    print("\n[Summary] Findings by severity:")
    for sev in ["critical", "high", "medium", "low", "info", "unknown"]:
        if severity_counter[sev]:
            print(f"  {sev.upper():9}: {severity_counter[sev]}")
