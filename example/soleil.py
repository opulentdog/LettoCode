import sys
sys.path.append('../lettocode/')

from lex_analysis import Lexer
from parser import LLParser
from turtle_interpretor import Interpretor,ScopeMemory
# Example usage
input_expression = """
name = input("Quel est la couleur du soleil? ");
if(name == "Jaune" || name == "Orange" || name=="Rouge"
|| name == "jaune" || name == "orange" || name=="Rouge"){
    x = 1;
    print("Oui le soleil est bien ");
    print(name);
    print("!\n");
}
else{
    y = 2;
    print("Le soleil n'est pas ");
    print(name);
    print(".\n");
}
"""

#Analyse lexicale
lexer=Lexer()
tokens=lexer.lex(input_expression)

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
