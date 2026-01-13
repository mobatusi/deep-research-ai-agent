import re

def clean_markdown(md_text: str) -> str:
    """
    Clean Markdown syntax from text to make it readable and suitable for display or PDF conversion.

    Args:
        md_text: Markdown-formatted text string

    Returns:
        Cleaned text with Markdown syntax removed
    """
    # Remove markdown headings (# ## ### etc.)
    text = re.sub(r'^#{1,6}\s+', '', md_text, flags=re.MULTILINE)

    # Remove bold formatting (**text**)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)

    # Remove italic formatting (*text*)
    text = re.sub(r'\*(.+?)\*', r'\1', text)

    # Remove inline code formatting (`code`)
    text = re.sub(r'`(.+?)`', r'\1', text)

    # Replace hyphen-based list items with bullet points
    text = re.sub(r'^-\s+', '• ', text, flags=re.MULTILINE)

    # Strip leading/trailing whitespace
    return text.strip()

