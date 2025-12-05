import os
import difflib
import requests
from dataclasses import dataclass

HF_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")

MODEL_ID = "Salesforce/codeT5-base"
HF_API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"


@dataclass
class PatchResponse:
    patched_snippet: str
    diff: str
    success: bool
    explanation: str
    model: str


class HFCloudPatchGenerator:

    def _diff(self, original: str, patched: str, filename="snippet") -> str:
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            patched.splitlines(keepends=True),
            fromfile=f"{filename} (original)",
            tofile=f"{filename} (patched)",
            lineterm=""
        )
        return "".join(diff)

    def generate(self, file_path, snippet, severity, model_outputs):
        if not HF_API_TOKEN:
            return PatchResponse(snippet, "", False, "HF token missing", MODEL_ID)

        prompt = f"""
Fix the security vulnerability in the following code:

{snippet}

Return only secure updated code. Do not add explanation.
        """

        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json",
        }

        payload = {"inputs": prompt}

        try:
            r = requests.post(HF_API_URL, headers=headers, json=payload)
            r.raise_for_status()

            output = r.json()

            # Response format: list of dicts with "generated_text"
            text = output[0].get("generated_text", "").strip()
            if not text:
                raise ValueError("Bad model output")

            diff = self._diff(snippet, text, file_path)

            return PatchResponse(
                patched_snippet=text,
                diff=diff,
                success=True,
                explanation="Patched via Hugging Face Inference API",
                model=MODEL_ID,
            )

        except Exception as e:
            return PatchResponse(snippet, "", False, f"HF error: {e}", MODEL_ID)
