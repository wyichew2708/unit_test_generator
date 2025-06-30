from dataclasses import dataclass
from typing import Optional

from agents.review_agent import ReviewAgent
from agents.test_generator_agent import TestGeneratorAgent, TestGenerationRequest
from agents.prompt_generator import PromptContext, PromptGenerator
from agents.repository_analyzer import RepositoryAnalyzer

@dataclass
class UserInput:
    repo_path: str
    target_file: str
    test_types: list[str]
    language: str
    framework: str
    output_mode: str
    user_prompt: str
    output_path: str

class FeedbackLoop:
    def __init__(self):
        self.prompt_gen = PromptGenerator()
        self.test_agent = TestGeneratorAgent()
        self.review_agent = ReviewAgent()

    def run(self, user_input: UserInput) -> str:
        analyzer = RepositoryAnalyzer(user_input.repo_path)
        summary = analyzer.analyze()
        context = PromptContext(
            user_prompt=user_input.user_prompt,
            target_language=user_input.language,
            test_types=user_input.test_types,
            framework=user_input.framework,
            repo_summary=summary,
            target_file=user_input.target_file,
        )
        prompt = self.prompt_gen.create_prompt(context)
        req = TestGenerationRequest(
            prompt=prompt,
            target_file=user_input.target_file,
            framework=user_input.framework,
            output_path=user_input.output_path,
        )
        iteration = 0
        while True:
            iteration += 1
            test_code = self.test_agent.generate(req)
            review = self.review_agent.review(test_code)
            if review.approved:
                break
            # Refine prompt with structured review feedback
            feedback_lines = "\n- ".join(review.comments)
            prompt += (
                "\n\nPlease update the tests addressing these comments:\n- "
                + feedback_lines
            )
            req.prompt = prompt
            if iteration > 3:  # prevent endless loops
                break
        return test_code
