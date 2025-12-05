# cyberwarrior/ai/devign_model.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

MODEL_NAME = "mahdin70/graphcodebert-devign-code-vulnerability-detector"


class DevignVulnerabilityModel:
    """
    Wrapper around GraphCodeBERT Devign model for vulnerability detection.
    We treat it as a text-classification model over code snippets.
    """

    def __init__(self):
        device = 0 if torch.cuda.is_available() else -1
        print(f"[Model:Devign] Loading on device: {device}")
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
            "model": "devign",
            "label": result["label"],
            "score": float(result["score"]),
        }
