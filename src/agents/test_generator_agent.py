import json
import os
from dataclasses import dataclass
from urllib import request

from ..utils import OllamaConfig, load_config

@dataclass
class TestGenerationRequest:
    prompt: str
    target_file: str
    framework: str
    output_path: str

class TestGeneratorAgent:
    """Agent responsible for calling LLM to create test script."""

    def __init__(self, config: OllamaConfig | None = None):
        self.config = config or load_config()

    def generate(self, req: TestGenerationRequest) -> str:
        payload = json.dumps(
            {
                "model": self.config.model,
                "prompt": req.prompt,
                "options": {
                    "temperature": self.config.temperature,
                    "top_p": self.config.top_p,
                    "top_k": self.config.top_k,
                    "num_predict": self.config.num_predict,
                },
            }
        ).encode("utf-8")
        try:
            req_obj = request.Request(
                self.config.api_url,
                data=payload,
                headers={"Content-Type": "application/json"},
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

TestGenerationRequest.__test__ = False  # prevent pytest from collecting
TestGeneratorAgent.__test__ = False  # prevent pytest from collecting
