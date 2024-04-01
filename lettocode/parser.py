from errors import ErrorHandler
from trees import Tree

errorhandler=ErrorHandler()

class LLParser:
    operators_hierarchy=[#[["INT_TYPE","STRING_TYPE"],1],
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
            errorhandler.syntax_error(self.error_message,self.error_index,self.tokens)
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

    def parse_term(self):#The returning value is an array of nodes
        inital_index=self.index
        initial_token=self.current_token

        token = self.current_token
        if token[0] in ["NUM","STRING","ID"]:
            self.current_token = self.get_next_token()
            if(token[0] == "ID" and self.current_token[0] == "LBRACKET"):#Liste
                index_token=self.parse_index()
                if index_token is None:
                    self.error_message="Invalid Index"
                    self.error_index = self.index-1
                    self.index=inital_index
                    self.current_token=initial_token
                    return None
                return [Tree(token,[Tree(["INDEX",""],[index_token])])]
            return [Tree(token)]
        elif token[0] == "LPAREN":
            nodes=[]
            retry=True
            while retry:
                self.current_token = self.get_next_token()
                node = self.parse_expression()
                if node is None:
                    self.error_message="Expected expression"
                    self.error_index = self.index-1
                    self.index=inital_index
                    self.current_token=initial_token
                    return None
                nodes+=node
                if self.current_token[0] != "COLON":
                    retry=False
            if self.current_token[0] != "RPAREN":
                self.error_message="Expected ')'"
                self.error_index = self.index-1
                self.index=inital_index
                self.current_token=initial_token
                return None
            self.current_token = self.get_next_token()
            return nodes
        elif token[0] == "LBRACKET":
            nodes=[]
            retry=True
            while retry:
                self.current_token = self.get_next_token()
                node = self.parse_expression()
                if node is None:
                    self.error_message="Expected expression"
                    self.error_index = self.index-1
                    self.index=inital_index
                    self.current_token=initial_token
                    return None
                nodes+=node
                if self.current_token[0] != "COLON":
                    retry=False
            if self.current_token[0] != "RBRACKET":
                self.error_message="Expected ')'"
                self.error_index = self.index-1
                self.index=inital_index
                self.current_token=initial_token
                return None
            self.current_token = self.get_next_token()
            return [Tree(["LIST",""],nodes)]
        else:
            self.error_message="Expected term"
            self.error_index = self.index-1
            self.index=inital_index
            self.current_token=initial_token
            return None
    def parse_expression(self,precedence=0):#The returning value is an array of nodes
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
                if node is None or (token[0] == "ID" and node[0].name[0]=="LIST"):#La deuxième partie de la condition permet de ne pas transformer les index en liste mais c'est du bricolage ex "s[0]=0" sinon "[0]" devient une liste et est passé en argument de la fonction s
                    self.index=inital_index
                    self.current_token=initial_token
                    self.error_message=initial_error_message
                    self.error_index=initial_error_index
                    #print(self.current_token)
                    return self.parse_expression(precedence+1)
                return [Tree([token[0], token[1]], node)]
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
                node = [Tree([token[0], token[1]], node+right)]
            return node
        else:
            raise Exception("L'arité de l'opérateur n'est pas supportée")
    def parse_single_expression(self):
        expr = self.parse_expression() 
        if(expr is None or len(expr)!=1):
            self.error_message="Expected a single expression" 
            self.error_index = self.index-1 
            return None
        return expr[0]
    def parse_expression_statement(self): 
        inital_index=self.index
        initial_token=self.current_token
        #First should be an expression 
        expr = self.parse_single_expression() 
        if(expr == None): 
            self.index=inital_index 
            self.current_token=initial_token 
            return None

        #Next token should be a semicolon 
        if self.current_token[0] == "SEMICOLON": 
            self.current_token = self.get_next_token() 
            return expr 
        elif self.error_message==None: 
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
            expr = self.parse_single_expression()
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
                self.error_index=initial_error_index
            self.index=inital_index
            self.current_token=initial_token
            return None
    def parse_index(self):
        inital_index=self.index
        initial_token=self.current_token
        #First token should be a left bracket
        if self.current_token[0] == "LBRACKET":
            self.current_token = self.get_next_token()
            #Next an expression
            node = self.parse_single_expression()
            #Finally a closing right bracket
            if self.current_token[0] != "RBRACKET":
                self.error_message="Expected ']'"
                self.error_index = self.index-1
                self.index=inital_index
                self.current_token=initial_token
                return None
            self.current_token = self.get_next_token()
            return node
        return None


    def parse_while(self):
        inital_index=self.index
        initial_token=self.current_token
        #First token should be a while
        print_token = self.current_token
        if print_token[0] == "WHILE":
            self.current_token = self.get_next_token()
            #Next should be an expression
            expr = self.parse_single_expression()
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


