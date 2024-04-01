import sys
sys.path.append('../obfuscator/')

from transform import TreeDecoder,SimpleParse,VariableModifier

# Example Usage
expr = """
print("True"+", notFalse");
print("This is cool");
print("Right?");
"""
tree=SimpleParse.parse_code(expr)
VariableModifier.strings_to_vars(tree)
#print(tree)
print(TreeDecoder.string_of_tree(tree))
