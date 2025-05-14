import litellm

DEFAULT_PROMPT_TEMPLATE = """You are an expert file format converter. Your sole task is to convert the following file content into well-formatted Markdown.
Analyze the content and structure it appropriately using Markdown syntax (headings, lists, code blocks, tables, emphasis, links if identifiable, etc.).
Ensure the output is *only* the Markdown content itself, without any introductory phrases, explanations, or concluding remarks.
"""

FILE_CONTENT_TEMPLATE = \
"""
File Content:
---
{content}
---
"""

def convert_to_markdown(
    content: str,
    model: str,
    api_key: str = None,
    base_url: str = None,
    custom_prompt_template: str = None,
) -> str:
    prompt_template = custom_prompt_template or DEFAULT_PROMPT_TEMPLATE
    prompt_template += FILE_CONTENT_TEMPLATE
    try:
        prompt = prompt_template.format(content=content)
    except KeyError:
        raise ValueError("Custom prompt template must include a '{content}' placeholder.")

    messages = [{"role": "user", "content": prompt}]

    response = litellm.completion(
        model=model,
        messages=messages,
        api_key=api_key,
        base_url=base_url,
    )
    markdown_output = response.choices[0].message.content
    return markdown_output.strip() if markdown_output else ""
