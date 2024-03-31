class Lexer:
    def __init__(self):
        self.tokens=[
                #["INT_TYPE",lambda s : self.match("int",s)],
                #["STRING_TYPE",lambda s : self.match("string",s)],
                ["IF",lambda s : self.match("if",s)],
                ["ELSE",lambda s : self.match("else",s)],
                ["WHILE",lambda s : self.match("while",s)],
                ["NUM", lambda s : self.match_num(s)],
                ["STRING", lambda s : self.match_string(s)],
                ["ID", lambda s : self.match_id(s)],
                ["ADD",lambda s : self.match("+", s)],
                ["SUB",lambda s : self.match("-",s)],
                ["MULT",lambda s : self.match("*",s)],
                ["DIV", lambda s : self.match("/",s)],
                ["BTW_RSHIFT", lambda s : self.match(">>",s)],
                ["BTW_LSHIFT", lambda s : self.match("<<",s)],
                ["EQUAL", lambda s : self.match("==",s)],
                ["NOTEQUAL", lambda s : self.match("!=",s)],
                ["LESSEQUAL", lambda s : self.match("<=",s)],
                ["LESS", lambda s : self.match("<",s)],
                ["GREATEREQUAL", lambda s : self.match(">=",s)],
                ["GREATER", lambda s : self.match(">",s)],
                ["NOT", lambda s : self.match("!",s)],
                ["AND", lambda s : self.match("&&",s)],
                ["OR", lambda s : self.match("||",s)],
                ["SET",lambda s : self.match("=",s)],
                ["MOD",lambda s : self.match("%",s)],
                ["BTW_AND", lambda s : self.match("&",s)],
                ["BTW_OR", lambda s : self.match("|",s)],
                ["BTW_XOR", lambda s : self.match("^",s)],
                ["BTW_NOT", lambda s : self.match("~",s)],
                ["WHITESPACE", lambda s : self.match_whitespace(s)],
                ["NEWLINE", lambda s : self.match("\n",s)],
                ["LPAREN", lambda s : self.match("(",s)],
                ["RPAREN", lambda s : self.match(")",s)],
                ["LBRACKET", lambda s : self.match("[",s)],
                ["RBRACKET" , lambda s : self.match("]",s)],
                ["LBRACE" , lambda s : self.match("{",s)],
                ["RBRACE" , lambda s : self.match("}",s)],
                ["COLON", lambda s : self.match(",",s)],
                ["SEMICOLON", lambda s : self.match(";",s)],
                ["END",lambda s : ["",s]],
                #Pour usage après l'analyse lexicale
                ["EXPR", lambda s : ["",s]],# 1+2+3*3*4*6
                ["SCOPE", lambda s : ["",s]],#{ ... code ... }
                ["INDEX", lambda s : ["",s]]]#arr[i]

    def match(self,expr, s):
        if s.startswith(expr):
            return [expr,s[len(expr):]]
        return ["",s]

    def match_num(self,s):
        i=0
        while(i < len(s) and (48<=ord(s[i]) and ord(s[i])<=57)):
            i+=1
        return [s[:i],s[i:]]

    def match_id(self,s):
        i=0
        while(i < len(s) and ((97<=ord(s[i]) and ord(s[i])<=122) or (65<=ord(s[i]) and ord(s[i])<=90))):
            i+=1
        return [s[:i],s[i:]]

    def match_string(self,s):
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

    def match_whitespace(self,s):
        i=0
        while(i < len(s) and (s[i] == " " or s[i] == "\t")):
            i+=1
        return [s[:i],s[i:]]

    def lex(self,s):
        tokenlist=[]
        while(s!=""):
            for token in self.tokens:
                parsed=token[1](s)
                if parsed[0] != "":
                    tokenlist.append([token[0],parsed[0]])
                    s=parsed[1]
                    break
                elif token[0] == "END":
                    print(f'Caractère illégal: "{s[0]}"')
                    exit()

        return tokenlist

