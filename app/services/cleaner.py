import re


def _remove_special_characters(text: str) -> str:
    return re.sub(r"[^\x00-\x7F]+", " ", text)


def _collapse_whitespace(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def _remove_soft_hyphens(text: str) -> str:
    return text.replace("\xad", "")


def _remove_non_breaking_spaces(text: str) -> str:
    return text.replace("\xa0", " ")


def _strip_lines(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(lines)


def clean_text(text: str) -> str:
    text = _remove_soft_hyphens(text)
    text = _remove_non_breaking_spaces(text)
    text = _remove_special_characters(text)
    text = _strip_lines(text)
    text = _collapse_whitespace(text)
    return text.strip()
