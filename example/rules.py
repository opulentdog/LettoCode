import sys
sys.path.append('../lettocode/')

from lex_analysis import Lexer
from parser import LLParser
from turtle_interpretor import Interpretor,ScopeMemory
# Example usage
input_expression = """2 + 3 * 4"""

#Analyse lexicale
lexer=Lexer()
tokens=lexer.lex(input_expression)

#Analyse syntaxique
parser=LLParser(tokens)
tree=parser.parse_expression()

print(tree[0])
exit()

#Interprétation de l'arbre
turtle=Interpretor(tree)
main_memory=ScopeMemory()

#print(turtle.current_node.childs)
turtle.execute_scope(turtle.current_node,main_memory,True)
