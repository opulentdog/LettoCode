import sys
sys.path.append('../obfuscator/')

from transform import TreeDecoder,SimpleParse,VariableModifier

# Example Usage
expr = """
x=53;
y=4;
if(x%y==1){
    print("True");
}
"""
tree=SimpleParse.parse_code(expr)
VariableModifier.randomize_variables(tree)
print(TreeDecoder.string_of_tree(tree))

