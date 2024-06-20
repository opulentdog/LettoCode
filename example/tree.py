import sys
sys.path.append('../lettocode/')

from lex_analysis import Lexer
from parser import LLParser
from turtle_interpretor import Interpretor,ScopeMemory
# Example usage
input_expression = """
int b = 0;
int a = 0;
while(b != 0){
    if(a > b){
        a = a - b;
    }else{
        b = b - a;
    }
}
"""

#Analyse lexicale
lexer=Lexer()
tokens=lexer.lex(input_expression)

#Analyse syntaxique
parser=LLParser(tokens)
tree=parser.parse()

print(tree)
exit()

#Interprétation de l'arbre
turtle=Interpretor(tree)
main_memory=ScopeMemory()

#print(turtle.current_node.childs)
turtle.execute_scope(turtle.current_node,main_memory,True)
