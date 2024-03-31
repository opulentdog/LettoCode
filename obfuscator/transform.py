class TreeDecoder:
    def get_rank(opp):
        hierarchy=[["INT_TYPE","STRING_TYPE"],
                         ["SET"], 
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
                         ["ID","NUM"]]

        for i in range(len(hierarchy)):
            if opp in hierarchy[i]:
                return i
        return -1

    def string_of_tree(node):
        if node.name[0] in ["ID","NUM"]:
            return node.name[1]
        rank=get_rank(node.name[0])
        if node.name[0] in ["ADD","SUB","MULT","DIV","EQUAL","MOD","NOT","SET","OR"] and len(node.childs) == 2:
            if get_rank(node.childs[0].name[0])<rank or rank==-1:
                right_term="("+string_of_tree(node.childs[0])+")"
            else: 
                right_term=string_of_tree(node.childs[0])
            if get_rank(node.childs[1].name[0])<rank or rank==-1:
                left_term="("+string_of_tree(node.childs[1])+")"
            else: 
                left_term=string_of_tree(node.childs[1])
            return right_term+node.name[1]+left_term
        if node.name[0] in ["BTW_NOT","ADD","SUB"] and len(node.childs) == 1:
            if get_rank(node.childs[0].name[0])<rank or rank==-1:
                return node.name[1]+"("+string_of_tree(node.childs[0])+")"
            else:
                return node.name[1]+string_of_tree(node.childs[0])
        print("Erreur: Arbre non supporté "+node.name[0])
        exit()

                        



# Example usage
input_expression = """
string name = input("Quel est la couleur du soleil? ");
if(name == "Jaune" || name == "Orange" || name="Rouge"){
    int x = 1;
    print("Oui le soleil est bien ");
    print(name);
    print("!\n");
}
else{
    int y = 2;
    print("Le soleil n'est pas");
    print(name);
    print(".\n");
}
"""




#turtle=interpretor(parsed_tree)
#main_memory=ScopeMemory()
#print(turtle.current_node.childs)
#turtle.execute_scope(turtle.current_node,main_memory,False)


def parse_expr(s):
    tokens = lex(s)
    parser = LLParser(tokens)
    return parser.parse_expression()

def parse_code(s):
    tokens = lex(s)
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
                new_tree = parse_expr(rule[1])
                self.substitute_nodes(new_tree, dic)
                node.childs[i]=new_tree
            else:
                self.apply_nodes(node.childs[i],rule_tree,rule)
        return string_of_tree(node)

    def apply_rule(self, rule, expr_string):
        expr_tree = parse_expr(expr_string)
        rule_tree = parse_expr(rule[0])
        dic=self.identification(expr_tree, rule_tree)
        if dic != None:
            new_tree = parse_expr(rule[1])
            self.substitute_nodes(new_tree, dic)
            expr_tree=new_tree
        return self.apply_nodes(expr_tree,rule_tree,rule)


class VariableModifier:
    def __init__(self,action_tree):
        pass
    def get_vars(self,node,variables=set()):
        if node != None:
            for child in node.childs:
                self.get_vars(child,variables)
            if node.name[0] == "ID" and len(node.childs)==0:
                variables.add(node.name[1])
        return variables
    def fusion(self,node1,node2):
        pass

input_expr = """
int x=input "input x";
int y=2;
x=x%y;
x=x*3;
"""


tree = parse_code(input_expr);
print(tree);
var_mod=VariableModifier(tree);
print(var_mod.get_vars(tree))





#expr="x*-2%4&1==2&&9/+y-2!=3"
#print(parse_expr(expr))
#exit();

# Example Usage
expr = "x%2==1"
rules = [
        ("a==b", "a==2*a-b"),
        ("a%b","((a*2)%(b*2))/2"),
        ("a=b","(c=b+a=c)/2")
        ]
#rule_applier = RuleApplier()
#result = rule_applier.apply_rule(rules[0], expr)
#result = rule_applier.apply_rule(rules[1], result)
#result = rule_applier.apply_rule(rules[2], result)
#print(result)
#print(parse_expr(result))


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
