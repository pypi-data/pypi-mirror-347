import json
import os


class JsonToMarkdownConverter:
    def __init__(self, json_data):
        """Initialize the converter with the parsed JSON data."""
        self.json_data = json_data
        # Build a mapping from block_id to block
        self.blocks = {}
        for block in self.json_data.get('items', []):
            self.blocks[block['block_id']] = block

    def get_text_from_elements(self, elements):
        """Extracts and concatenates text from a list of text elements."""
        text = ''
        for elem in elements:
            if 'text_run' in elem:
                text += elem['text_run'].get('content', '')
            elif 'equation' in elem:
                # For equations, we simply output the content (optionally wrap in $ if needed)
                text += elem['equation'].get('content', '')
        return text

    def convert_block(self, block, header_level=1, indent=''):
        """Recursively converts a single block (and its children) to Markdown."""
        markdown = ''
        bt = block.get('block_type')

        # Process block content based on its type
        if bt == 1:
            # Container / page block. It may contain a page with elements (title).
            if 'page' in block and 'elements' in block['page']:
                content = self.get_text_from_elements(block['page']['elements']).strip()
                if content:
                    markdown += indent + '# ' + content + '\n\n'
        elif bt == 2:
            # Paragraph block with text
            if 'text' in block and 'elements' in block['text']:
                content = self.get_text_from_elements(block['text']['elements']).strip()
                markdown += indent + content + '\n\n'
        elif bt == 3:
            # Heading block (heading1) -> convert to a markdown header
            if 'heading1' in block and 'elements' in block['heading1']:
                content = self.get_text_from_elements(block['heading1']['elements']).strip()
                markdown += indent + ('#' * header_level) + ' ' + content + '\n\n'
        elif bt == 12:
            # Unordered list item (bullet).
            if 'bullet' in block and 'elements' in block['bullet']:
                content = self.get_text_from_elements(block['bullet']['elements']).strip()
                markdown += indent + '- ' + content + '\n'
        elif bt == 13:
            # Ordered list item
            if 'ordered' in block and 'elements' in block['ordered']:
                content = self.get_text_from_elements(block['ordered']['elements']).strip()
                markdown += indent + '1. ' + content + '\n'
        elif bt == 27:
            # Image block: output a markdown image using the token as a placeholder
            if 'image' in block:
                token = block['image'].get('token', 'Image')
                markdown += indent + '![Image](' + token + ')\n\n'
        else:
            # Fallback: if the block has a text field, output it
            if 'text' in block and 'elements' in block['text']:
                content = self.get_text_from_elements(block['text']['elements']).strip()
                markdown += indent + content + '\n\n'

        # Process children recursively if any
        if 'children' in block and block['children']:
            # For list items, we want to indent nested children
            if bt in [12, 13]:
                child_indent = indent + '  '
            else:
                child_indent = indent
            # Increase header level for headings under container blocks
            child_header_level = header_level + 1 if bt in [1, 3] else header_level

            for child_id in block['children']:
                child = self.blocks.get(child_id)
                if child:
                    markdown += self.convert_block(child, header_level=child_header_level, indent=child_indent)
        
        return markdown

    def convert(self):
        """Converts the entire JSON document to a Markdown string."""
        markdown = ''
        # Process blocks that are top-level (parent_id is an empty string)
        for block in self.json_data.get('items', []):
            if block.get('parent_id', '') == '':
                markdown += self.convert_block(block, header_level=1, indent='') + '\n'
        return markdown


# Example usage:
if __name__ == '__main__':
    dir = os.path.dirname(__file__)
    # Load the JSON file (update the file path as needed)
    with open(os.path.join(dir, 'block_data.json'), 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    converter = JsonToMarkdownConverter(json_data)
    markdown_output = converter.convert()
    
    # 将Markdown结果保存到文件
    output_file_path = os.path.join(dir, 'output.md')
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_output)
    
    print(f"Markdown content has been saved to {output_file_path}") 