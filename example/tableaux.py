import sys
sys.path.append('../lettocode/')#Bricolage :)

from lex_analysis import Lexer
from parser import LLParser
from turtle_interpretor import Interpretor,ScopeMemory
# Example usage
input_expression = """
s="hey";
print(s);
"""

#Analyse lexicale
lexer=Lexer()
tokens=lexer.lex(input_expression)
#print(tokens)

#Analyse syntaxique
parser=LLParser(tokens)
tree=parser.parse()

#print(tree)
#exit()

#Interprétation de l'arbre
turtle=Interpretor(tree)
main_memory=ScopeMemory()

#print(turtle.current_node.childs)
turtle.execute_scope(turtle.current_node,main_memory,True)
