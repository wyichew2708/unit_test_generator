from dataclasses import dataclass
import json
import os
from typing import Optional

@dataclass
class OllamaConfig:
    model: str = "qwen2.5-coder:7b"
    api_url: str = "http://localhost:11434/api/generate"
    temperature: float = 0.0
    top_p: float = 1.0
    top_k: int = 40
    num_predict: int = 256


def load_config(path: Optional[str] = None) -> OllamaConfig:
    config = OllamaConfig()
    file_path = path or os.environ.get("OLLAMA_CONFIG")
    if file_path and os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        for key in config.__dataclass_fields__:
            if key in data:
                setattr(config, key, data[key])
    return config
