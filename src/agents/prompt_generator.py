from dataclasses import dataclass
from typing import List

from .repository_analyzer import RepositorySummary

@dataclass
class PromptContext:
    user_prompt: str
    target_language: str
    test_types: List[str]
    framework: str
    repo_summary: RepositorySummary

class PromptGenerator:
    """Build prompts for LLM based on collected context."""

    def create_prompt(self, context: PromptContext) -> str:
        parts = [
            "User prompt:\n" + context.user_prompt,
            f"Target language: {context.target_language}",
            f"Testing framework: {context.framework}",
            "Types of tests: " + ', '.join(context.test_types),
            "Repository summary:",
        ]
        for file in context.repo_summary.files:
            parts.append(f"- {file.path}")
            for func in file.functions:
                parts.append(f"  * {func.name}({', '.join(func.args)})")
        parts.append("Expected outcome: Well-structured test scripts")
        return '\n'.join(parts)
