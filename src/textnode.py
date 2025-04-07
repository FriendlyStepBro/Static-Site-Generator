from enum import Enum

class TextType(Enum):
    NORMAL = 'normal'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode():
    def __init__(self, text: str, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        text = self.text == other.text
        text_type = self.text_type == other.text_type
        url = self.url == other.url
        return text and text_type and url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"