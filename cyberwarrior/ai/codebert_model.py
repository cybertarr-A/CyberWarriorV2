import random


class CodeBERTVulnerabilityModel:
    """CodeBERT Vulnerability Model - using mock predictions for demo"""
    
    def __init__(self):
        print("[Model] CodeBERT Vulnerability Model initialized (mock mode)")
        self.model = None
        # Pattern-based vulnerability detection for demo
        self.vulnerable_patterns = [
            "eval(",
            "exec(",
            "os.system(",
            "subprocess.call(",
            "sql(",
            "query(",
            "insert into",
            "delete from",
            "drop table",
            "__import__",
            "pickle.loads(",
            "yaml.load(",
            "jsonpickle",
        ]

    def predict(self, text: str):
        """
        Simple pattern-based vulnerability detection
        Returns a vulnerability prediction
        """
        text_lower = text.lower()
        
        # Check for vulnerable patterns
        found_patterns = [p for p in self.vulnerable_patterns if p in text_lower]
        
        if found_patterns:
            # Higher confidence for found patterns
            score = min(0.99, 0.5 + len(found_patterns) * 0.15)
            return {
                "label": "VULNERABILITY",
                "score": score,
                "patterns": found_patterns
            }
        
        # Random low confidence for safe code
        score = random.random() * 0.3
        return {
            "label": "NO_VULNERABILITY",
            "score": score,
            "patterns": []
        }
