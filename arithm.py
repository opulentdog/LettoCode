
file=open("input.txt")
entree=file.readlines()

def match(expr, s):
    if s.startswith(expr):
        return [expr,s[len(expr):]]
    return ["",s]

def match_num(s):
    i=0
    while(i < len(s) and (48<=ord(s[i]) and ord(s[i])<=57)):
        i+=1
    return [s[:i],s[i:]]

def match_id(s):
    i=0
    while(i < len(s) and ((97<=ord(s[i]) and ord(s[i])<=122) or (65<=ord(s[i]) and ord(s[i])<=90))):
        i+=1
    return [s[:i],s[i:]]

def match_string(s):
    #Check if first character is bettween quotes
    if s[0] != "\"":
        return ["",s]
    else:
        i=1
        while(i < len(s) and s[i] != "\""):
            i+=1
        if i >= len(s):
            return ["",s]
        else:
            return ["\""+s[1:i]+"\"",s[i+1:]]

def match_whitespace(s):
    i=0
    while(i < len(s) and (s[i] == " " or s[i] == "\t")):
        i+=1
    return [s[:i],s[i:]]

tokens=[["INT_TYPE",lambda s : match("int",s)],
        ["STRING_TYPE",lambda s : match("string",s)],
        ["IF",lambda s : match("if",s)],
        ["ELSE",lambda s : match("else",s)],
        ["WHILE",lambda s : match("while",s)],
        ["NUM", lambda s : match_num(s)],
        ["STRING", lambda s : match_string(s)],
        ["ID", lambda s : match_id(s)],
        ["ADD",lambda s : match("+", s)],
        ["SUB",lambda s : match("-",s)],
        ["MULT",lambda s : match("*",s)],
        ["DIV", lambda s : match("/",s)],
        ["BTW_RSHIFT", lambda s : match(">>",s)],
        ["BTW_LSHIFT", lambda s : match("<<",s)],
        ["EQUAL", lambda s : match("==",s)],
        ["NOTEQUAL", lambda s : match("!=",s)],
        ["LESSEQUAL", lambda s : match("<=",s)],
        ["LESS", lambda s : match("<",s)],
        ["GREATEREQUAL", lambda s : match(">=",s)],
        ["GREATER", lambda s : match(">",s)],
        ["NOT", lambda s : match("!",s)],
        ["AND", lambda s : match("&&",s)],
        ["OR", lambda s : match("||",s)],
        ["SET",lambda s : match("=",s)],
        ["MOD",lambda s : match("%",s)],
        ["BTW_AND", lambda s : match("&",s)],
        ["BTW_OR", lambda s : match("|",s)],
        ["BTW_XOR", lambda s : match("^",s)],
        ["BTW_NOT", lambda s : match("~",s)],
        ["WHITESPACE", lambda s : match_whitespace(s)],
        ["NEWLINE", lambda s : match("\n",s)],
        ["LPAREN", lambda s : match("(",s)],
        ["RPAREN", lambda s : match(")",s)],
        #["LBRACKET", lambda s : match("[",s)],#Listes pour plus tard
        #["RBRACKET" , lambda s : match("]",s)],
        ["LBRACE" , lambda s : match("{",s)],
        ["RBRACE" , lambda s : match("}",s)],
        ["SEMICOLON", lambda s : match(";",s)],
        ["END",lambda s : ["",s]],
        #Pour usage après l'analyse lexicale
        ["EXPR", lambda s : ["",s]],# 1+2+3*3*4*6
        ["SCOPE", lambda s : ["",s]],#{ ... code ... }
        ["INDEX", lambda s : ["",s]]]#arr[i]



def lex(s):
    tokenlist=[]
    while(s!=""):
        for token in tokens:
            parsed=token[1](s)
            if parsed[0] != "":
                tokenlist.append([token[0],parsed[0]])
                s=parsed[1]
                break
            elif token[0] == "END":
                print(f'Caractère illégal: "{s[0]}"')
                exit()

    return tokenlist

class Tree:
    def __init__(self, name=['root',''], childs=None): #Racine
        self.name = name
        self.childs = []
        if childs is not None:
            for child in childs:
                self.add(child)
    def __repr__(self):
        return self.repr_name(self)+"\n"+"\n".join(self.array_arbre(self))
    def add(self, node):
        assert isinstance(node, Tree)
        self.childs.append(node)
    def repr_name(self,a):
        return repr(a.name)
        if len(a.name)!=2:
            return a.name
        if a.name[0] in ["ID","STRING","NUM"]:
            return f"{a.name[0]}:"+a.name[1].replace('\n','\\n')
        return a.name[0]
    def array_arbre(self,a):
        s=[]
        if a.childs:
            offset=(len(self.repr_name(a))-1)
            #offset=4
            for child in a.childs[:-1]:
                s+=[("├"+"─"*offset)+self.repr_name(child)]
                r=self.array_arbre(child)
                for line in r:
                    s+=["│"+" "*offset+line]
                #s.append("")
            s+=[("└"+"─"*offset)+self.repr_name(a.childs[-1])]
            r=self.array_arbre(a.childs[-1])
            for line in r:
                s+=[" "+" "*offset+line]
        return s


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def string_of_tokenlist(tokens):
    return "".join([token[1] for token in tokens])
def pos_of_token(index,tokens):
    i=index
    pos=0
    while(i>0):
        i-=1
        pos+=len(tokens[i][1])
    return pos

def syntax_error(msg,index,tokens):
    line=0
    column=0
    linestart=0
    for i in range(0,index):
        column+=1
        if tokens[i][0] == "NEWLINE":
            line+=1
            column=0
            linestart=i
    lineend=linestart+1
    while(lineend<len(tokens) and tokens[lineend][0]!="NEWLINE"):
        lineend+=1
    line_tokens=tokens[linestart+1:lineend]
    print(bcolors.BOLD + "Ligne: "+ bcolors.ENDC + str(line)+bcolors.BOLD + "\nColonne: "+ bcolors.ENDC + str(pos_of_token(column,line_tokens)))
    print("\t"+string_of_tokenlist(line_tokens))
    print(bcolors.FAIL + "\t"+" "*pos_of_token(column,line_tokens)+"^" + bcolors.ENDC)
    print(bcolors.FAIL +"Erreur de Syntaxe"+ bcolors.ENDC+": "+msg)
    print(tokens[index:index+2])
    #exit()
    raise Exception(msg)



class LLParser:
    operators_hierarchy=[[["INT_TYPE","STRING_TYPE"],1],
                     [["SET"],2], 
                     [["AND","OR"],2],
                     [["NOT"],1],
                     [["EQUAL","NOTEQUAL","LESSEQUAL",
                       "LESS","GREATER","GREATEREQUAL"],2],
                     [["ADD","SUB"],2],
                     [["MOD"],2],
                     [["DIV","MULT"],2],
                     [["BTW_RSHIFT","BTW_LSHIFT"],2],
                     [["BTW_AND","BTW_OR","BTW_XOR"],2],
                     [["ADD","SUB"],1],
                     [["BTW_NOT"],1],
                     [["ID"],1]]#Fonctions

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.current_token = None
        self.current_token = self.get_next_token()
        self.error_index = None
        self.error_message = None

    def parse(self):
        statements = self.parse_statements()
        if statements == [] or self.get_next_token() != ["END",""]:
            syntax_error(self.error_message,self.error_index,self.tokens)
        return Tree('root',statements)

    def get_next_token(self,skip_newline=True,skip_whitespace=True):
        if self.index < len(self.tokens):
            token = self.tokens[self.index]
            self.index += 1
            if token[0]=="NEWLINE" and skip_newline:
                return self.get_next_token()
            if token[0]=="WHITESPACE" and skip_whitespace:
                return self.get_next_token()
            return token
        return ["END", ""]

    def parse_term(self):
        inital_index=self.index
        initial_token=self.current_token

        token = self.current_token
        if token[0] in ["NUM","STRING","ID"]:
            self.current_token = self.get_next_token()
            return Tree(token)
        elif token[0] == "LPAREN":
            self.current_token = self.get_next_token()
            node = self.parse_expression()
            if self.current_token[0] != "RPAREN":
                self.error_message="Expected ')'"
                self.error_index = self.index-1
                self.index=inital_index
                self.current_token=initial_token
                return None
            self.current_token = self.get_next_token()
            return node
        else:
            self.error_message="Expected term"
            self.error_index = self.index-1
            self.index=inital_index
            self.current_token=initial_token
            return None
    def parse_expression(self,precedence=0):
        inital_index=self.index
        initial_token=self.current_token
        initial_error_message=self.error_message
        initial_error_index=self.error_index
        if precedence == len(self.operators_hierarchy):
            #print("Parsing term",self.current_token)
            return self.parse_term()
        elif self.operators_hierarchy[precedence][1] == 1:#Opérateur Unaire
            if self.current_token[0] in self.operators_hierarchy[precedence][0]:
                #print("unary",self.operators_hierarchy[precedence][0]);
                token = self.current_token
                self.current_token = self.get_next_token()
                node = self.parse_expression(precedence)
                if node is None:
                    self.index=inital_index
                    self.current_token=initial_token
                    self.error_message=initial_error_message
                    self.error_index=initial_error_index
                    #print(self.current_token)
                    return self.parse_expression(precedence+1)
                return Tree([token[0], token[1]], [node])
            else:
                return self.parse_expression(precedence+1)
        elif self.operators_hierarchy[precedence][1] == 2:#Opérateur Binaire
            node = self.parse_expression(precedence+1)
            if node is None:
                self.index=inital_index
                self.current_token=initial_token
                return None
            while self.current_token[0] in self.operators_hierarchy[precedence][0]:
                #print("operator",self.operators_hierarchy[precedence][0]);
                token = self.current_token
                self.current_token = self.get_next_token()
                right = self.parse_expression(precedence+1)
                if right is None:
                    self.index=inital_index
                    self.current_token=initial_token
                    return None
                node = Tree([token[0], token[1]], [node, right])
            return node
        else:
            raise Exception("L'arité de l'opérateur n'est pas supportée")
    def parse_expression_statement(self): 
        inital_index=self.index
        initial_token=self.current_token
        #First should be an expression 
        expr = self.parse_expression() 
        if(expr == None): 
            self.index=inital_index 
            self.current_token=initial_token 
            return None 
        
        #Next token should be a semicolon 
        if self.current_token[0] == "SEMICOLON": 
            self.current_token = self.get_next_token() 
            return expr 
        else: 
            self.error_message="Expected ';'" 
            self.error_index = self.index-1 
            return None
    def parse_statement(self):
        #print("1")
        inital_index=self.index
        initial_token=self.current_token
        if self.current_token[0] in ["IF"]:
            #print("parse if",self.current_token)
            if_statement = self.parse_if()
            if if_statement is not None:
                return if_statement
        if self.current_token[0] in ["WHILE"]:
            while_statement = self.parse_while()
            if while_statement is not None:
                return while_statement
        if  self.current_token[0] in ["LBRACE"]:
            #print("parsed block")
            block=self.parse_block()
            if block is not None:
                return block
            #print("Failed")
        if self.current_token[0] in ["RBRACE"]:
            return None
        if self.error_message==None:
            #print("parse expression statement",self.current_token)
            expression = self.parse_expression_statement()
            if expression is not None:
                return expression
        if self.error_message==None:
            self.error_message="Expected statement"
            self.error_index = self.index-1
        self.index=inital_index
        self.current_token=initial_token
        return None
    def parse_statements(self):
        inital_index=self.index
        initial_token=self.current_token
        statement = self.parse_statement()
        statements = []
        while statement is not None:
            statements.append(statement)
            statement=self.parse_statement()
        return statements
    def parse_block(self):
        inital_index=self.index
        initial_token=self.current_token
        #First token should be a left brace
        if self.current_token[0] == "LBRACE":
            self.current_token = self.get_next_token()
            #Next should be statements
            statements = self.parse_statements()
            if statements is None:
                self.index=inital_index
                self.current_token=initial_token
                return None
            #Next token should be a right brace
            if self.current_token[0] == "RBRACE":
                self.current_token = self.get_next_token()
                return Tree(["SCOPE",""],statements)
            else:
                self.error_message="Expected '}'"
                self.error_index = self.index-1
                self.index=inital_index
                self.current_token=initial_token
                return None
        else:
            self.error_message="Expected '{'"
            self.error_index = self.index-1
            self.index=inital_index
            self.current_token=initial_token
            return None
    def parse_if(self):
        inital_index=self.index
        initial_token=self.current_token
        #First token should be a if
        print_token = self.current_token
        if print_token[0] == "IF":
            self.current_token = self.get_next_token()
            #Next should be an expression
            expr = self.parse_expression()
            if(expr == None):
                self.index=inital_index
                self.current_token=initial_token
                return None
            #Next should be a code block
            block = self.parse_block()
            if(block == None):
                self.index=inital_index
                self.current_token=initial_token
                return None
            parsed_else= self.parse_else(False)
            if(parsed_else != None):
                return Tree(["IF",""],[expr,block,parsed_else])
            return Tree(["IF",""],[expr,block])
        else:
            self.error_message="Expected if"
            self.error_index = self.index-1
            self.index=inital_index
            self.current_token=initial_token
            return None
    def parse_else(self,save_state=True):
        inital_index=self.index
        initial_token=self.current_token
        initial_error=self.error_message
        initial_error_index=self.error_index

        #First token should be a if
        print_token = self.current_token
        if print_token[0] == "ELSE":
            self.current_token = self.get_next_token()
            #Next should be a code block
            block = self.parse_block()
            if(block == None):
                self.index=inital_index
                self.current_token=initial_token
                if not save_state:
                    self.error_message=initial_error
                    self.error_index=initial_error_index
                return None
            return Tree(["ELSE",""],[block])
        else:
            if save_state:
                self.error_message="Expected ELSE"
                self.error_index = self.index-1
            else:
                self.error_message=initial_error
                self.error_index=inital_error_index
            self.index=inital_index
            self.current_token=initial_token
            return None



    def parse_while(self):
        inital_index=self.index
        initial_token=self.current_token
        #First token should be a while
        print_token = self.current_token
        if print_token[0] == "WHILE":
            self.current_token = self.get_next_token()
            #Next should be an expression
            expr = self.parse_expression()
            if(expr == None):
                self.index=inital_index
                self.current_token=initial_token
                return None
            #Next should be a code block
            block = self.parse_block()
            if(block == None):
                self.index=inital_index
                self.current_token=initial_token
                return None
            return Tree(["WHILE",""],[expr,block])

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
#input_expression="1+1+2*2/2"#Probleme avec l'erreur
#expr="(((1+1)+(1+1))+((1+1)+(1+1)))+(((1+1)+(1+1))+((1+1)+(21+1)));"
#tokens = lex(input_expression)

#parser = LLParser(tokens)
#parsed_tree = parser.parse()
#print(parsed_tree)
#exit()

#Thoughts on the interpretor
#The interpretor can execute statements
#Maybe we will add semantic analysis before the interpretor

#Check if the left argument of set is a variable.

#but I think the issues will become more clear when I start writting the interpretor
#

class ScopeMemory:
    def __init__(self):
        self.memory = {}
        self.parent = None
    def set(self, name, value,create):
        if create:
            self.memory[name] = value
        else:
            if name in self.memory:
                self.memory[name] = value
            elif self.parent is not None:
                self.parent.set(name,value,False)
            else:
                raise Exception("Variable not defined")
    def get(self, name):
        if name in self.memory:
            return self.memory[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            return None

class interpretor():
    def __init__(self,action_tree):
        self.initial_tree=action_tree
        self.current_node=action_tree
        self.error_index=None#Maybe for later,
        #by adding a third element containing the index to tokens during parsing
        self.error_message=None
    def calculate_expression(self,node,scope_memory,create):
        if node == None:
            node = self.current_node
        if scope_memory == None:
            raise Exception("Scope memory is not defined")
        operators=[["ADD",2,lambda a,b: a+b],
                    ["ADD",1,lambda a: a],
                    ["SUB",2,lambda a,b: a-b],
                    ["SUB",1,lambda a: -a],
                    ["MULT",2,lambda a,b: a*b],
                    ["DIV",2,lambda a,b: a//b],
                    ["MOD",2,lambda a,b: a%b],
                    ["EQUAL",2,lambda a,b: a==b],
                    ["NOTEQUAL",2,lambda a,b: a!=b],
                    ["LESS",2,lambda a,b: a<b],
                    ["LESSEQUAL",2,lambda a,b: a<=b],
                    ["GREATER",2,lambda a,b: a<=b],
                    ["GREATEREQUAL",2,lambda a,b: a<=b],
                    ["NOT",1,lambda a: not a]]
        #This function can either return an int or a string
        if node.name[0] in ["INT_TYPE","STRING_TYPE"]:
            self.calculate_expression(node.childs[0],scope_memory,True)
        if node.name == ["ID","print"]:
            print(self.calculate_expression(node.childs[0],scope_memory,False),end="")
            return 0
        if node.name == ["ID","input"]:
            return input(self.calculate_expression(node.childs[0],scope_memory,False))
        if node.name[0] == "ID":
            return scope_memory.get(node.name[1])
        if node.name[0] == "NUM":
            return int(node.name[1])
        if node.name[0] == "STRING":
            return node.name[1][1:-1]
        if node.name[0] == "SET":
            r=self.calculate_expression(node.childs[1],scope_memory,create)
            scope_memory.set(node.childs[0].name[1],r,create)
            #print(scope_memory.memory)
            return r
        for operator in operators:
            if node.name[0] == operator[0] and len(node.childs)==operator[1]:
                #print(node.name[0],len(node.childs))
                args=()
                for child in node.childs:
                    args+=(self.calculate_expression(child,scope_memory,False),)
                return operator[2](*args)
    def execute_statement(self,node,scope_memory):
        if node.name[0] == "SCOPE":
            self.execute_scope(node,scope_memory,True)
        elif node.name[0] == "IF":
            if_scope_memory=ScopeMemory()
            if_scope_memory.parent=scope_memory
            if self.calculate_expression(node.childs[0],if_scope_memory,False):
                self.execute_scope(node.childs[1],if_scope_memory,False)
            elif len(node.childs) == 3 and node.childs[2].name[0] == "ELSE":
                self.execute_scope(node.childs[2].childs[0],if_scope_memory,False)
        elif node.name[0] == "WHILE":
            #exit()
            while_scope_memory=ScopeMemory()
            while_scope_memory.parent=scope_memory
            while self.calculate_expression(node.childs[0],while_scope_memory,False):
                self.execute_scope(node.childs[1],while_scope_memory,False)
                #print(self.calculate_expression(node.childs[0],while_scope_memory))
        else:
            self.calculate_expression(node,scope_memory,False)
    def execute_scope(self,node,parent_memory,new_scope):
        #if not node.name[0] == "SCOPE":
        #    raise Exception("Expected scope")
        if new_scope:
            new_scope_memory=ScopeMemory()
            new_scope_memory.parent=parent_memory
        else:
            new_scope_memory=parent_memory
        for statement in node.childs:
            #print(statement.name[0])
            self.execute_statement(statement,new_scope_memory)


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

#print(parse_code(input_expr))
