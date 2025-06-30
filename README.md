# Unit Test Generator

This project provides a simple command line interface to generate test scripts
using language models. The process is broken down into several agents that
analyze the repository, build prompts and review generated code. All LLM calls
are routed to an on-premise [Ollama](https://ollama.com/) instance.

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
You can also supply extra instructions with `--prompt` when calling the CLI.
The tool sends prompts to an on-premise Ollama instance to generate tests. Set
`OLLAMA_API_URL` if your server is not running on `http://localhost:11434`.
By default, it calls the `qwen2.5-coder:7b` model available in Ollama. Prompts
now include a short repository summary and are automatically refined using any
feedback from the review agent.

You can provide a JSON configuration file to tweak generation parameters such as
model, API URL, temperature and context length. Pass the file path with `--config`:

```bash
python -m src.main --repo <path> --file <target_file> --config ollama_config.json
```

Example `ollama_config.json`:

```json
{
  "model": "qwen2.5-coder:7b",
  "api_url": "http://localhost:11434/api/generate",
  "temperature": 0.0,
  "top_p": 1.0,
  "top_k": 40,
  "num_predict": 256,
  "context_length": 4096
}
```

## Streamlit Interface

You can also launch a simple web UI using Streamlit. The interface allows you to
select a repository, choose a target file and configure test generation options.

```bash
streamlit run src/ui/app.py
```

The generated tests can be downloaded directly from the interface or displayed
on the page.
