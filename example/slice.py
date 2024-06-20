import sys
sys.path.append('../obfuscator/')

from transform import TreeDecoder,SimpleParse,VariableModifier

# Example Usage
expr = """
text="Hello, World!\n"
print(text)
"""
tree=SimpleParse.parse_code(expr)
VariableModifier.slice_variables(tree)
print(TreeDecoder.string_of_tree(tree))

