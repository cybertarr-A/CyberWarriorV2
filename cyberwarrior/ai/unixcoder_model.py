# cyberwarrior/ai/unixcoder_model.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

MODEL_NAME = "mahdin70/unixcoder-code-vulnerability-detector"


class UnixCoderVulnerabilityModel:
    """
    Wrapper around UniXCoder vulnerability detector.
    """

    def __init__(self):
        device = 0 if torch.cuda.is_available() else -1
        print(f"[Model:UnixCoder] Loading on device: {device}")
        self.pipeline = pipeline(
            "text-classification",
            model=MODEL_NAME,
            tokenizer=MODEL_NAME,
            device=device,
            top_k=1,
        )

    def predict(self, text: str):
        text = text[:512]
        result = self.pipeline(text)[0]
        return {
            "model": "unixcoder",
            "label": result["label"],
            "score": float(result["score"]),
        }
