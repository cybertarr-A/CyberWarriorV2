import argparse
import json
from tqdm import tqdm
from cyberwarrior.repo.github_loader import clone_repo_or_load_path, find_code_files
from cyberwarrior.analysis.analyzer import Analyzer


def run_scan(github_url: str, output_file: str):
    repo_path = clone_repo_or_load_path(github_url)
    analyzer = Analyzer()

    results = {}
    files = list(find_code_files(repo_path))

    print(f"[Scan] Total code files found: {len(files)}\n")

    for file in tqdm(files, desc="Analyzing files"):
        findings = analyzer.analyze_file(file)
        if findings:
            results[file] = findings

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n[✔] Scan complete! Results saved to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CyberWarrior V2 - AI Bug Bounty Tool")
    parser.add_argument("repo", help="GitHub Repository URL")
    parser.add_argument("--out", default="scan_results.json", help="Output JSON file")

    args = parser.parse_args()
    run_scan(args.repo, args.out)
