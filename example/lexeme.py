import sys
sys.path.append('../lettocode/')

from lex_analysis import Lexer
from parser import LLParser
from interpretor import Interpretor,ScopeMemory
# Example usage
input_expression = """result=a+b*c;"""

#Analyse lexicale
lexer=Lexer()
tokens=lexer.lex(input_expression)

#Analyse syntaxique
parser=LLParser(tokens)
tree=parser.parse()

print([noi[0] for noi in tokens])
exit()

#Interprétation de l'arbre
turtle=Interpretor(tree)
main_memory=ScopeMemory()

#print(turtle.current_node.childs)
turtle.execute_scope(turtle.current_node,main_memory,True)
