import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def get_block_type(text):
    match text[0]:
        case '#':
            if is_heading(text): return BlockType.HEADING
        case '`':
            if is_code(text): return BlockType.CODE
        case '>':
            if is_quote(text): return BlockType.QUOTE
        case '-':
            if is_unordered_list(text): return BlockType.UNORDERED_LIST
        case '1':
            if is_ordered_list(text): return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
            
        

def is_heading(text):
    # Check if text starts with 1-6 '#' followed by a space
    pattern = r"^#{1,6}\s"
    return re.match(pattern, text) is not None


def is_code(text):
    # Check if text starts with ``` and ends with ```
    pattern = r"^```[\s\S]+```$"
    return re.match(pattern, text, re.DOTALL) is not None


def is_quote(text):
    # Check if every line starts with '>'
    pattern = r"^(?:>.*(?:\n|$))+$"
    return re.fullmatch(pattern, text, flags=re.MULTILINE) is not None


def is_unordered_list(text):
    # Check if every line starts with a '- '
    # Updated pattern: each line must match "- " followed by any number of non-newline characters.
    pattern = r"^(?:-\s[^\n]*(?:\n|$))+$"
    return re.fullmatch(pattern, text) is not None


def is_ordered_list(text):
    # Check if each line starts with an incrementing number followed by ". "
    pattern = r"^(?P<num>\d+)\.\s.*(?:\n|$)"
    lines = text.splitlines(keepends=True)
    expected = 1
    for line in lines:
        m = re.match(pattern, line)
        if not m or int(m.group("num")) != expected:
            return False
        expected += 1
    return True

