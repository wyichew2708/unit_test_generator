import argparse
from utils.feedback_loop import FeedbackLoop, UserInput


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate unit tests with AI")
    parser.add_argument('--repo', required=True, help='Path to repository')
    parser.add_argument('--file', required=True, help='Target file to test')
    parser.add_argument('--types', nargs='+', default=['unit'], help='Types of tests')
    parser.add_argument('--language', default='python', help='Target language')
    parser.add_argument('--framework', default='pytest', help='Testing framework')
    parser.add_argument('--output', default='download', choices=['download', 'repo'], help='Output mode')
    parser.add_argument('--prompt', default='')
    parser.add_argument('--output-path', default='generated_tests/test_generated.py')
    parser.add_argument('--config', default=None, help='Path to Ollama config file')
    args = parser.parse_args()

    loop = FeedbackLoop(config_path=args.config)
    user_input = UserInput(
        repo_path=args.repo,
        target_file=args.file,
        test_types=args.types,
        language=args.language,
        framework=args.framework,
        output_mode=args.output,
        user_prompt=args.prompt,
        output_path=args.output_path,
    )
    test_code = loop.run(user_input)
    if args.output == 'download':
        print(test_code)
    else:
        print(f"Test written to {args.output_path}")


if __name__ == '__main__':
    main()
