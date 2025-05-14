import click
import pathlib
from .converter import convert_to_markdown
from . import __version__

@click.command()
@click.option(
    "-i", "--input", "input_file",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=pathlib.Path),
    required=True,
    help="Path to the input file to convert."
)
@click.option(
    "-o", "--output", "output_file",
    type=click.Path(dir_okay=False, writable=True, path_type=pathlib.Path),
    required=True,
    help="Path to save the output Markdown file."
)
@click.option(
    "-m", "--model",
    default="gpt-4.1-nano",
    show_default=True,
    help="The LLM model to use for conversion (e.g., gpt-4o, claude-3-opus-20240229)."
)
@click.option(
    "-p", "--prompt", "prompt_template",
    help="Custom prompt template. Must include '{content}' placeholder for the file content."
)
@click.option(
    "--api-key",
    help="API key for the LLM provider. Overrides environment variables."
)
@click.option(
    "--base-url",
    help="Custom base URL for the LLM API (e.g., for local LLMs or proxies)."
)
@click.version_option(__version__, package_name="any-to-md-cli")
def main(
    input_file: pathlib.Path,
    output_file: pathlib.Path,
    model: str,
    prompt_template: str,
    api_key: str,
    base_url: str
):
    """Converts various file formats to Markdown using AI (litellm)."""

    click.echo(f"Reading content from: {input_file}")
    try:
        content = input_file.read_text(encoding="utf-8")
    except Exception as e:
        click.secho(f"Error reading input file: {e}", fg="red", err=True)
        raise click.Abort()

    click.echo(f"Converting content using model: {model}...")
    try:
        markdown_output = convert_to_markdown(content, model, api_key, base_url, prompt_template)
        output_file.write_text(markdown_output, encoding="utf-8")
        click.secho(f"Successfully converted and saved to: {output_file}", fg="green")
    except Exception as e:
        click.secho(f"Error during conversion or writing output: {e}", fg="red", err=True)
        raise click.Abort()

if __name__ == '__main__':
    main()
