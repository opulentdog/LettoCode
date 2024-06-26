import sys
sys.path.append('../obfuscator/')

from transform import TreeDecoder,SimpleParse,VariableModifier

# Example Usage
expr = """
z=1;
y=4;
{
    x=53;
    if(x%y==1){
        print("True");
    }
}
"""
tree=SimpleParse.parse_code(expr)
VariableModifier.randomize_variables(tree)
print(TreeDecoder.string_of_tree(tree))

