# Any-to-MD CLI

A command-line tool that uses AI (via `litellm`) to convert various file contents into Markdown format.

## Features

- Converts content from a specified input file.
- Outputs well-formatted Markdown to a specified output file.
- Leverages Large Language Models (LLMs) through `litellm` for versatile conversion.
- Supports various LLM providers and models configurable via `litellm`.
- Allows custom prompt templates for tailored conversions.

## Installation
```bash
pip install any-to-md-cli
```

## API Key Configuration

This tool relies on `litellm`, which requires API keys for the chosen LLM provider (e.g., OpenAI, Anthropic, Cohere, etc.).

You **MUST** set the appropriate environment variable for the LLM provider you intend to use. For example:

- For OpenAI models (like `gpt-3.5-turbo`, `gpt-4`): `export OPENAI_API_KEY="your_openai_api_key"`
- For Anthropic models (like `claude`): `export ANTHROPIC_API_KEY="your_anthropic_api_key"`

Refer to the [LiteLLM documentation](https://docs.litellm.ai/docs/providers) for a comprehensive list of supported providers and their required environment variables. You can also pass the API key directly using the `--api-key` option.

## Usage
```bash
any-to-md-cli --input path/to/your/input.file --output path/to/your/output.md
```

**Options:**

-   `-i, --input FILE_PATH`: Path to the input file (Required).
-   `-o, --output FILE_PATH`: Path to the output Markdown file (Required).
-   `-m, --model MODEL_NAME`: Specify the LLM model to use (e.g., `gpt-4o`, `claude-3-opus-20240229`). Defaults to `gpt-3.5-turbo`.
-   `-p, --prompt PROMPT_TEMPLATE`: Custom prompt template. Must include `{content}` placeholder.
-   `--api-key YOUR_API_KEY`: Directly provide the API key for the LLM.
-   `--base-url YOUR_BASE_URL`: Specify a custom base URL for API calls.
-   `--version`: Show the version and exit.
-   `--help`: Show this message and exit.

**Example with default prompt:**
```bash
any-to-md-cli -i notes.txt -o notes.md -m gpt-4o
```

**Example with custom prompt:**
```bash
any-to-md-cli -i code.py -o code_explanation.md -m gpt-4o -p "Explain the following Python code and provide usage examples in Markdown format."
```
