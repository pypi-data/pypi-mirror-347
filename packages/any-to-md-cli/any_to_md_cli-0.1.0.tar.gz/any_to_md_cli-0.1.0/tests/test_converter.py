import pytest
from unittest.mock import MagicMock
from any_to_md_cli.converter import convert_to_markdown, DEFAULT_PROMPT_TEMPLATE, FILE_CONTENT_TEMPLATE


def test_convert_to_markdown_default_prompt(mocker):
    mock_completion = mocker.patch("litellm.completion")
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Mocked Markdown Output"
    mock_completion.return_value = mock_response

    file_content = "This is some test content."
    model = "test-model"

    result = convert_to_markdown(file_content, model)

    expected_prompt = DEFAULT_PROMPT_TEMPLATE + FILE_CONTENT_TEMPLATE.format(content=file_content)
    mock_completion.assert_called_once_with(
        model=model,
        messages=[{"role": "user", "content": expected_prompt}],
        api_key=None,
        base_url=None,
    )
    assert result == "Mocked Markdown Output"


def test_convert_to_markdown_custom_prompt(mocker):
    mock_completion = mocker.patch("litellm.completion")
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Custom Mocked Output"
    mock_completion.return_value = mock_response

    file_content = "Another test content."
    model = "custom-model"
    custom_prompt = "Convert this: {content}"

    result = convert_to_markdown(file_content, model, custom_prompt_template=custom_prompt)

    expected_prompt = (custom_prompt + FILE_CONTENT_TEMPLATE).format(content=file_content)
    mock_completion.assert_called_once_with(
        model=model,
        messages=[{"role": "user", "content": expected_prompt}],
        api_key=None,
        base_url=None,
    )
    assert result == "Custom Mocked Output"


def test_convert_to_markdown_api_key_and_base_url(mocker):
    mock_completion = mocker.patch("litellm.completion")
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "API Key Test Output"
    mock_completion.return_value = mock_response

    file_content = "Content with API key."
    model = "api-model"
    api_key = "test_api_key"
    base_url = "http://localhost:8000"

    result = convert_to_markdown(file_content, model, api_key=api_key, base_url=base_url)

    expected_prompt = DEFAULT_PROMPT_TEMPLATE + FILE_CONTENT_TEMPLATE.format(content=file_content)
    mock_completion.assert_called_once_with(
        model=model,
        messages=[{"role": "user", "content": expected_prompt}],
        api_key=api_key,
        base_url=base_url,
    )
    assert result == "API Key Test Output"


def test_convert_to_markdown_empty_response_from_llm(mocker):
    mock_completion = mocker.patch("litellm.completion")
    mock_response = MagicMock()
    mock_completion.return_value = mock_response

    mock_response.choices[0].message.content = None
    assert convert_to_markdown("content", "model") == ""

    mock_response.choices[0].message.content = "   "
    assert convert_to_markdown("content", "model") == ""
