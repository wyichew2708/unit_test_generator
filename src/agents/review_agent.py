from dataclasses import dataclass
from typing import List

@dataclass
class ReviewResult:
    comments: List[str]
    approved: bool

class ReviewAgent:
    """Analyze generated test code and provide feedback."""

    def review(self, test_code: str) -> ReviewResult:
        comments = []
        if 'TODO' in test_code:
            comments.append('Remove TODO comments from tests.')
        if 'assert' not in test_code:
            comments.append('No assertions found in tests.')
        approved = len(comments) == 0
        return ReviewResult(comments=comments, approved=approved)
