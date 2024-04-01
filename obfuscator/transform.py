import math
import random
import string

import sys
sys.path.append('../lettocode/')

from lex_analysis import Lexer
from parser import LLParser
from trees import Tree

class TreeDecoder:
    def get_rank(opp):
        hierarchy=[["SET"], 
                         ["AND","OR"],
                         ["NOT"],
                         ["EQUAL","NOTEQUAL","LESS","LESSEQUAL","GREATER","GREATEREQUAL"],
                         ["ADD","SUB"],
                         ["MOD"],
                         ["DIV","MULT"],
                         ["BTW_RSHIFT","BTW_LSHIFT"],
                         ["BTW_AND","BTW_OR","BTW_XOR"],
                         ["ADD","SUB"],
                         ["BTW_NOT"],
                         ["ID","NUM","STRING"]]

        for i in range(len(hierarchy)):
            if opp in hierarchy[i]:
                return i
        return -1

    def string_of_tree(node):
        if node.name == "root":
            r=""
            r+=TreeDecoder.string_of_tree(node.childs[0])+";"
            for child in node.childs[1:]:
                r+="\n"+TreeDecoder.string_of_tree(child)
                if r[-1]!="}":
                    r+=";"
            return r
        if node.name[0] == "IF" and len(node.childs)==2:
            r="if("+TreeDecoder.string_of_tree(node.childs[0])+")"
            r+=TreeDecoder.string_of_tree(node.childs[1])
            return r
        if node.name[0] == "SCOPE":
            r="{\n"
            for child in node.childs:
                statement=TreeDecoder.string_of_tree(child)
                statement="\n".join(["    "+line for line in statement.split("\n")])
                r+=statement
                if r[-1]!="}":
                    r+=";"
                r+="\n"
            r+="}"
            return r
        if node.name[0] in ["ID","NUM","STRING"]:
            if len(node.childs)>=1:
                args="("+TreeDecoder.string_of_tree(node.childs[0])
                for child in node.childs[1:]:
                    r+=","+TreeDecoder.string_of_tree(child)
                args+=")"
                return node.name[1]+args
            else:
                return node.name[1]
        rank=TreeDecoder.get_rank(node.name[0])
        if node.name[0] in ["ADD","SUB","MULT","DIV","EQUAL","MOD","NOT","SET","OR"] and len(node.childs) == 2:
            if TreeDecoder.get_rank(node.childs[0].name[0])<rank or rank==-1:
                right_term="("+TreeDecoder.string_of_tree(node.childs[0])+")"
            else: 
                right_term=TreeDecoder.string_of_tree(node.childs[0])
            if TreeDecoder.get_rank(node.childs[1].name[0])<rank or rank==-1:
                left_term="("+TreeDecoder.string_of_tree(node.childs[1])+")"
            else:
                left_term=TreeDecoder.string_of_tree(node.childs[1])
            return right_term+node.name[1]+left_term
        if node.name[0] in ["BTW_NOT","ADD","SUB"] and len(node.childs) == 1:
            if TreeDecoder.get_rank(node.childs[0].name[0])<rank or rank==-1:
                return node.name[1]+"("+TreeDecoder.string_of_tree(node.childs[0])+")"
            else:
                return node.name[1]+TreeDecoder.string_of_tree(node.childs[0])
        print("Erreur: Arbre non supporté "+repr(node.name))
        exit()             

class SimpleParse:
    def parse_expr(s):
        lexer=Lexer()
        tokens = lexer.lex(s)
        parser = LLParser(tokens)
        return parser.parse_single_expression()

    def parse_code(s):
        lexer=Lexer()
        tokens = lexer.lex(s)
        parser = LLParser(tokens)
        return parser.parse()

class RuleApplier:
    
    def identification(self, node, rule_node,dic={}):
        if rule_node.name[0] == "ID":
            dic[rule_node.name[1]] = node
            return dic

        if node.name[0] != rule_node.name[0] or len(node.childs) != len(rule_node.childs):
            return None

        for i in range(len(node.childs)):
            if self.identification(node.childs[i], rule_node.childs[i],dic) is None:
                return None

        return dic

    def substitute_nodes(self, node, dic):
        for i in range(len(node.childs)):
            if node.childs[i].name[0] == "ID" and dic[node.childs[i].name[1]] is not None:
                node.childs[i] = dic[node.childs[i].name[1]]
            else:
                self.substitute_nodes(node.childs[i], dic)

    def apply_nodes(self,node,rule_tree,rule):
        for i in range(len(node.childs)):
            if (dic:=self.identification(node.childs[i],rule_tree)) != None:
                new_tree = SimpleParse.parse_expr(rule[1])
                self.substitute_nodes(new_tree, dic)
                node.childs[i]=new_tree
            else:
                self.apply_nodes(node.childs[i],rule_tree,rule)
        return TreeDecoder.string_of_tree(node)

    def apply_rule(self, rule, expr_string):
        expr_tree = SimpleParse.parse_expr(expr_string)
        rule_tree = SimpleParse.parse_expr(rule[0])
        dic=self.identification(expr_tree, rule_tree)
        if dic != None:
            new_tree = SimpleParse.parse_expr(rule[1])
            self.substitute_nodes(new_tree, dic)
            expr_tree=new_tree
        return self.apply_nodes(expr_tree,rule_tree,rule)


class VariableModifier:
    def get_vars(node,variables={},current_scope=None):
        """
        Cette fonction renvoie un dictionnaire dans lequel les
        clés sont les noms de variables et on pour valeur une liste
        des instructions dans lesquels apparaissent la variables
        """
        if node != None:
            if node.name[0] == "SCOPE":
                current_scope=node
            for child in node.childs:
                VariableModifier.get_vars(child,variables,current_scope)
            if node.name[0] == "ID" and len(node.childs)==0:
                if node.name[1] in variables:
                    variables[node.name[1]].append([current_scope,node])
                else:
                    variables[node.name[1]]=[[current_scope,node]]
        return variables
    def generate_unique_strings(n, k=-1):
        """
        Cette fonction génère une liste de `n` chaînes
        de caractères uniques, chacune ayant une taille de `k`.

        Paramètres :
            - n : Nombre de chaînes de caractères à générer.
            - k : Taille de chaque chaîne de caractères.

        Retourne :
            Une liste contenant `n` chaînes 
            de caractères uniques, chacune ayant une taille de `k`.

        La fonction vérifie que le nombre total de chaînes 
        demandées est inférieur ou égal au nombre total possible 
        de chaînes de caractères uniques de taille `k`.
        """
        if k == -1:
            k = math.ceil(math.log(n, 26))
            k=max(k,5)

        if n * k > 26 ** k:
            raise ValueError("Il est impossible de générer des chaînes uniques. Trop de chaînes ont été demandées pour la taille donnée")

        strings = set()
        while len(strings) < n:
            new_string = ''.join(random.choices(string.ascii_lowercase, k=k))
            strings.add(new_string)
        
        return list(strings)
    def generate_unique_variable(existing_variables,base_name='var',index=1):
        while True:
            new_variable = f'{base_name}{index}'
            if new_variable not in existing_variables:
                return new_variable
            index += 1
    def randomize_variables(node):
        var_dict=VariableModifier.get_vars(node)
        var_names=list(var_dict.keys())
        new_names=VariableModifier.generate_unique_strings(len(var_names))
        for i in range(len(var_names)):
            for occurence in var_dict[var_names[i]]:
                occurence[1].name[1]=new_names[i]
    def strings_to_vars(node,current_scope=None):
        var_dict=VariableModifier.get_vars(node)
        var_names=list(var_dict.keys())
        def aux_strings_to_vars(node,current_scope=None):
            if node != None:
                if node.name[0] == "SCOPE" or node.name=="root":
                    current_scope=node
                if node.name[0] != "SET":#Ignore variable affectation
                    if node.name[0] == "STRING" and len(node.childs)==0:
                        if current_scope is None:
                            print(current_scope)
                            raise Exception("Impossible de déterminer le scope de l'instruction.")
                        new_name=VariableModifier.generate_unique_variable(var_names,"str")
                        var_names.append(new_name)
                        set_node=Tree(["SET","="],[],current_scope)
                        set_node.add(Tree(["ID",new_name]))
                        set_node.add(Tree(["STRING",node.name[1]]))
                        current_scope.childs.insert(0,set_node)
                        node.name[0]="ID"
                        node.name[1]=new_name
                    for child in node.childs:
                        aux_strings_to_vars(child,current_scope)
        aux_strings_to_vars(node)
    def fusion(node1,node2):
        pass

input_expr = """
int x=input "input x";
int y=2;
x=x%y;
x=x*3;
"""


#tree = parse_code(input_expr);
#print(tree);
#var_mod=VariableModifier(tree);
#print(var_mod.get_vars(tree))





#expr="x*-2%4&1==2&&9/+y-2!=3"
#print(parse_expr(expr))
#exit();




input_expr = """
string text = "Hello World\n";
print(text);
int x = 1;
x=x+1;
print(x);
x=x-2;
"""

input_expr = """
int x=0
x=x+4

int y=7

y=7+x
x=5

"""


input_expr = """
int x =4;
"""

#
