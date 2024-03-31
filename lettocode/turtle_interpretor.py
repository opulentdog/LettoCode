class ScopeMemory:
    def __init__(self):
        self.memory = {}
        self.parent = None
    def set(self, name, value):
        if name in self.memory:
            self.memory[name] = value
        elif self.parent is not None:
            self.parent.set(name,value)
        else:
            self.memory[name] = value
    def get(self, name):
        if name in self.memory:
            return self.memory[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            raise Exception("Variable not defined")

class Interpretor():
    def __init__(self,action_tree):
        self.initial_tree=action_tree
        self.current_node=action_tree
        self.error_index=None#For later,
        #adding a third element containing the index of the tokens during parsing
        #to track error position when encountering a failure at runtime
        self.error_message=None
    def calculate_expression(self,node,scope_memory):
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
                    ["OR",2,lambda a,b: a or b],
                    ["AND",2,lambda a,b: a and b],
                    ["NOT",1,lambda a: not a]]
        #This function can either return an int or a string
        if node.name[0] in ["INT_TYPE","STRING_TYPE"]:
            self.calculate_expression(node.childs[0],scope_memory)
        if node.name == ["ID","print"]:
            print(self.calculate_expression(node.childs[0],scope_memory),end="")
            return 0
        if node.name == ["ID","input"]:
            return input(self.calculate_expression(node.childs[0],scope_memory))
        if node.name[0] == "ID":
            if len(node.childs) == 1 and node.childs[0].name[0] == "INDEX":
                index_expr_node=node.childs[0].childs[0]
                index=self.calculate_expression(index_expr_node,scope_memory)
                return scope_memory.get(node.name[1])[index]
            else:
                return scope_memory.get(node.name[1])
        if node.name[0] == "NUM":
            return int(node.name[1])
        if node.name[0] == "STRING":
            return node.name[1][1:-1]
        if node.name[0] == "SET":
            r=self.calculate_expression(node.childs[1],scope_memory)
            if len(node.childs[0].childs) == 1 and node.childs[0].childs[0].name[0] == "INDEX":
                index_expr_node=node.childs[0].childs[0].childs[0]
                index=self.calculate_expression(index_expr_node,scope_memory)
                scope_memory.get(node.childs[0].name[1])[index]=r
            else:
                scope_memory.set(node.childs[0].name[1],r)
            return r
        for operator in operators:
            if node.name[0] == operator[0] and len(node.childs)==operator[1]:
                args=()
                for child in node.childs:
                    args+=(self.calculate_expression(child,scope_memory),)
                return operator[2](*args)
    def execute_statement(self,node,scope_memory):
        if node.name[0] == "SCOPE":
            self.execute_scope(node,scope_memory,True)
        elif node.name[0] == "IF":
            if_scope_memory=ScopeMemory()
            if_scope_memory.parent=scope_memory
            if self.calculate_expression(node.childs[0],if_scope_memory):
                self.execute_scope(node.childs[1],if_scope_memory)
            elif len(node.childs) == 3 and node.childs[2].name[0] == "ELSE":
                self.execute_scope(node.childs[2].childs[0],if_scope_memory,False)
        elif node.name[0] == "WHILE":
            while_scope_memory=ScopeMemory()
            while_scope_memory.parent=scope_memory
            while self.calculate_expression(node.childs[0],while_scope_memory):
                self.execute_scope(node.childs[1],while_scope_memory,False)
        else:
            self.calculate_expression(node,scope_memory)
    def execute_scope(self,node,parent_memory,new_scope):
        #if not node.name[0] == "SCOPE":
        #    raise Exception("Expected scope")
        if new_scope:
            new_scope_memory=ScopeMemory()
            new_scope_memory.parent=parent_memory
        else:
            new_scope_memory=parent_memory
        for statement in node.childs:
            self.execute_statement(statement,new_scope_memory)

