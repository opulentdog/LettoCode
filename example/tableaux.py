import sys
sys.path.append('../lettocode/')

from lex_analysis import Lexer
from parser import LLParser
from interpretor import Interpretor,ScopeMemory

# Example usage
input_expression = """
s1="Hello";
s2=" Wor";
s3="ld!\n";
print(s1+s2+s3);
"""

#Analyse lexicale
lexer=Lexer()
tokens=lexer.lex(input_expression)
#print(tokens)

#Analyse syntaxique
parser=LLParser(tokens)
tree=parser.parse()

print(tree)
#exit()

#Interprétation de l'arbre
turtle=Interpretor(tree)
main_memory=ScopeMemory()

#print(turtle.current_node.childs)
turtle.execute_scope(turtle.current_node,main_memory,True)
