from lex_analysis import Lexer
from parser import LLParser
from interpretor import Interpretor,ScopeMemory
# Example usage
input_expression = """
string name = input("Quel est la couleur du soleil? ");
if(name == "Jaune" || name == "Orange" || name=="Rouge"
|| name == "jaune" || name == "orange" || name=="rouge"){
    int x = 1;
    print("Oui le soleil est bien ");
    print(name);
    print("!\n");
}
else{
    int y = 2;
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

#Interprétation de l'arbre
turtle=Interpretor(tree)
main_memory=ScopeMemory()

turtle.execute_scope(turtle.current_node,main_memory,True)
