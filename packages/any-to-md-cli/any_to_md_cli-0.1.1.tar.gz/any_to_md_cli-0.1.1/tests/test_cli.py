import pytest
from click.testing import CliRunner
from any_to_md_cli.cli import main
from any_to_md_cli import __version__


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_successful_conversion(runner, tmp_path, mocker):
    mock_convert = mocker.patch("any_to_md_cli.cli.convert_to_markdown")
    mock_convert.return_value = "## Converted Content"

    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.md"
    input_file.write_text("Hello world")

    result = runner.invoke(main, ["-i", str(input_file), "-o", str(output_file)])

    assert result.exit_code == 0
    assert f"Reading content from: {input_file}" in result.output
    assert "Converting content using model: gpt-4.1-nano..." in result.output
    assert f"Successfully converted and saved to: {output_file}" in result.output
    assert output_file.read_text() == "## Converted Content"
    mock_convert.assert_called_once_with(
        "Hello world", "gpt-4.1-nano", None, None, None
    )


def test_cli_custom_options(runner, tmp_path, mocker):
    mock_convert = mocker.patch("any_to_md_cli.cli.convert_to_markdown")
    mock_convert.return_value = "## Custom Converted"

    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.md"
    input_file.write_text("Custom input")

    model = "custom-gpt"
    prompt = "Custom prompt: {content}"
    api_key = "testkey123"
    base_url = "http://custom.api"

    result = runner.invoke(main, [
        "-i", str(input_file),
        "-o", str(output_file),
        "-m", model,
        "-p", prompt,
        "--api-key", api_key,
        "--base-url", base_url
    ])

    assert result.exit_code == 0
    assert f"Converting content using model: {model}..." in result.output
    assert output_file.read_text() == "## Custom Converted"
    mock_convert.assert_called_once_with(
        "Custom input", model, api_key, base_url, prompt
    )


def test_cli_input_file_not_found(runner, tmp_path):
    output_file = tmp_path / "output.md"
    non_existent_input = tmp_path / "non_existent.txt"

    result = runner.invoke(main, ["-i", str(non_existent_input), "-o", str(output_file)])

    assert result.exit_code != 0
    assert "Error: Invalid value for '-i' / '--input': File" in result.output
    assert f"'{non_existent_input}' does not exist." in result.output


def test_cli_input_file_read_error(runner, tmp_path, mocker):
    mocker.patch("pathlib.Path.read_text", side_effect=IOError("Read permission denied"))
    input_file = tmp_path / "input.txt"
    input_file.write_text("content") # File must exist for click's Path(exists=True)

    result = runner.invoke(main, ["-i", str(input_file), "-o", str(tmp_path / "output.md")])

    assert result.exit_code == 1
    assert "Error reading input file: Read permission denied" in result.output


def test_cli_conversion_error(runner, tmp_path, mocker):
    mocker.patch("any_to_md_cli.cli.convert_to_markdown", side_effect=Exception("LLM API Error"))
    input_file = tmp_path / "input.txt"
    input_file.write_text("Hello world")

    result = runner.invoke(main, ["-i", str(input_file), "-o", str(tmp_path / "output.md")])

    assert result.exit_code == 1
    assert "Error during conversion or writing output: LLM API Error" in result.output


def test_cli_output_file_write_error(runner, tmp_path, mocker):
    mocker.patch("any_to_md_cli.cli.convert_to_markdown", return_value="## Content")

    input_file = tmp_path / "input.txt"
    input_file.write_text("Hello world")

    mocker.patch("pathlib.Path.write_text", side_effect=IOError("Disk full"))

    result = runner.invoke(main, ["-i", str(input_file), "-o", str(tmp_path / "output.md")])

    assert result.exit_code == 1
    assert "Error during conversion or writing output: Disk full" in result.output


def test_cli_version(runner):
    result = runner.invoke(main, ["--version"], prog_name="any-to-md-cli")
    assert result.exit_code == 0
    assert f"any-to-md-cli, version {__version__}" in result.output