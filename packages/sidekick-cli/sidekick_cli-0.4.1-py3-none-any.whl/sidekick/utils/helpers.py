import difflib
import io
import os
import sys
from contextlib import contextmanager

from rich.text import Text


class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


@contextmanager
def capture_stdout():
    """
    Context manager to capture stdout output.

    Example:
        with capture_stdout() as stdout_capture:
            print("This will be captured")

        captured_output = stdout_capture.getvalue()

    Returns:
        StringIO object containing the captured output
    """
    stdout_capture = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = stdout_capture
    try:
        yield stdout_capture
    finally:
        sys.stdout = original_stdout


def key_to_title(key):
    """
    Convert key to title, replacing underscores with spaces and capitalizing words.

    Replace words found in `UPPERCASE_WORDS` with their uppercase version.
    """
    UPPERCASE_WORDS = {"api", "id", "url"}
    words = key.split("_")
    result_words = []
    for word in words:
        lower_word = word.lower()
        if lower_word in UPPERCASE_WORDS:
            result_words.append(lower_word.upper())
        elif word:
            result_words.append(word[0].upper() + word[1:].lower())
        else:
            result_words.append("")

    return " ".join(result_words)


def ext_to_lang(path):
    """
    Get the language from the file extension. Default to `text` if not found.
    """
    MAP = {
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "java": "java",
        "c": "c",
        "cpp": "cpp",
        "cs": "csharp",
        "html": "html",
        "css": "css",
        "json": "json",
        "yaml": "yaml",
        "yml": "yaml",
    }
    ext = os.path.splitext(path)[1][1:]
    if ext in MAP:
        return MAP[ext]
    return "text"


def render_file_diff(target: str, patch: str, colors=None) -> Text:
    """
    Create a formatted diff between target and patch text.

    Args:
        target (str): The original text to be replaced.
        patch (str): The new text to insert.
        colors (dict, optional): Dictionary containing style colors.
                                If None, no styling will be applied.

    Returns:
        Text: A Rich Text object containing the formatted diff.
    """
    # Create a clean diff with styled text
    diff_text = Text()

    # Get lines and create a diff sequence
    target_lines = target.splitlines()
    patch_lines = patch.splitlines()

    # Use difflib to identify changes
    matcher = difflib.SequenceMatcher(None, target_lines, patch_lines)

    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            # Unchanged lines
            for line in target_lines[i1:i2]:
                diff_text.append(f"  {line}\n")
        elif op == "delete":
            # Removed lines - show in red with (-) prefix
            for line in target_lines[i1:i2]:
                if colors:
                    diff_text.append(f"- {line}\n", style=colors.error)
                else:
                    diff_text.append(f"- {line}\n")
        elif op == "insert":
            # Added lines - show in green with (+) prefix
            for line in patch_lines[j1:j2]:
                if colors:
                    diff_text.append(f"+ {line}\n", style=colors.success)
                else:
                    diff_text.append(f"+ {line}\n")
        elif op == "replace":
            # Removed lines with (-) prefix
            for line in target_lines[i1:i2]:
                if colors:
                    diff_text.append(f"- {line}\n", style=colors.error)
                else:
                    diff_text.append(f"- {line}\n")
            # Added lines with (+) prefix
            for line in patch_lines[j1:j2]:
                if colors:
                    diff_text.append(f"+ {line}\n", style=colors.success)
                else:
                    diff_text.append(f"+ {line}\n")

    return diff_text
