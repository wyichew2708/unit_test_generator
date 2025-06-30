import json
import os
from dataclasses import dataclass

from urllib import request

@dataclass
class TestGenerationRequest:
    prompt: str
    target_file: str
    framework: str
    output_path: str

class TestGeneratorAgent:
    """Agent responsible for calling LLM to create test script."""

    def __init__(self, model: str = "qwen2.5-coder:7b"):
        self.model = model
        self.api_url = os.environ.get(
            "OLLAMA_API_URL", "http://localhost:11434/api/generate"
        )

    def generate(self, req: TestGenerationRequest) -> str:
        payload = json.dumps({"model": self.model, "prompt": req.prompt}).encode(
            "utf-8"
        )
        try:
            req_obj = request.Request(
                self.api_url, data=payload, headers={"Content-Type": "application/json"}
            )
            with request.urlopen(req_obj, timeout=60) as res:
                data = json.load(res)
            test_code = data.get("response", "")
        except Exception:
            return "# Failed to contact LLM endpoint."
        os.makedirs(os.path.dirname(req.output_path), exist_ok=True)
        with open(req.output_path, "w", encoding="utf-8") as fh:
            fh.write(test_code)
        return test_code
