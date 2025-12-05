import os
import tempfile
import git


ALLOWED_EXTENSIONS = [
    ".py", ".js", ".ts", ".php", ".java",
    ".c", ".cpp", ".go", ".rb"
]


def clone_repo_or_load_path(path_or_url: str) -> str:
    # Local path support (offline mode)
    if os.path.exists(path_or_url):
        print(f"[Repo] Using local directory: {path_or_url}")
        return path_or_url

    # GitHub clone fallback
    temp_dir = tempfile.mkdtemp(prefix="cw_v2_")
    print(f"[Repo] Cloning: {path_or_url}")

    try:
        git.Repo.clone_from(
            path_or_url,
            temp_dir,
            depth=1,
            multi_options=["--no-single-branch"],
            config='http.sslVerify=false'
        )
        print(f"[Repo] Cloned to {temp_dir}")
        return temp_dir

    except Exception as e:
        print(f"[Error] Failed to clone GitHub repo: {e}")
        print("[Repo] Please provide a local path instead.")
        raise RuntimeError("Network or GitHub access error")


def find_code_files(base_path: str):
    for root, _, files in os.walk(base_path):
        for filename in files:
            if any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                yield os.path.join(root, filename)
