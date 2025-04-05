from textnode import *

def main():
    print('hello world')
    test_node = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")
    print(test_node)

if __name__ == "__main__":
    main()