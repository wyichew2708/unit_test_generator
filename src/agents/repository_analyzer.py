import os
import ast
from dataclasses import dataclass, field
from typing import List

@dataclass
class FunctionInfo:
    name: str
    args: List[str]

@dataclass
class FileSummary:
    path: str
    functions: List[FunctionInfo] = field(default_factory=list)

@dataclass
class RepositorySummary:
    files: List[FileSummary] = field(default_factory=list)

class RepositoryAnalyzer:
    """Parse a repository and extract high level information."""

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def analyze(self) -> RepositorySummary:
        summary = RepositorySummary()
        for root, _, files in os.walk(self.repo_path):
            for name in files:
                if name.endswith('.py'):
                    path = os.path.join(root, name)
                    file_summary = FileSummary(path=path)
                    with open(path, 'r', encoding='utf-8') as fh:
                        try:
                            tree = ast.parse(fh.read())
                        except SyntaxError:
                            continue
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            args = [arg.arg for arg in node.args.args]
                            file_summary.functions.append(FunctionInfo(name=node.name, args=args))
                    summary.files.append(file_summary)
        return summary
