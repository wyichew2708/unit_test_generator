# Unit Test Generator

This project provides a simple command line interface to generate test scripts
using language models. The process is broken down into several agents that
analyze the repository, build prompts and review generated code.

## Installation

Install the Python dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m src.main --repo <path> --file <target_file>
```

Additional flags allow you to customise framework, language and output mode.
The tool attempts to call OpenAI to generate tests. If the dependency is not
available, a placeholder message is returned.

## Streamlit Interface

You can also launch a simple web UI using Streamlit. The interface allows you to
select a repository, choose a target file and configure test generation options.

```bash
streamlit run src/ui/app.py
```

The generated tests can be downloaded directly from the interface or displayed
on the page.
