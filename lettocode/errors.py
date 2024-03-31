class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ErrorHandler:
    def __init__(self):
        self.test=[]#pass don't work
    def string_of_tokenlist(self,tokens):
        return "".join([token[1] for token in tokens])
    def pos_of_token(self,index,tokens):
        i=index
        pos=0
        while(i>0):
            i-=1
            pos+=len(tokens[i][1])
        return pos

    def syntax_error(self,msg,index,tokens):
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
        print(bcolors.BOLD + "Ligne: "+ bcolors.ENDC + str(line)+bcolors.BOLD + "\nColonne: "+ bcolors.ENDC + str(self.pos_of_token(column,line_tokens)))
        print("\t"+self.string_of_tokenlist(line_tokens))
        print(bcolors.FAIL + "\t"+" "*self.pos_of_token(column,line_tokens)+"^" + bcolors.ENDC)
        print(bcolors.FAIL +"Erreur de Syntaxe"+ bcolors.ENDC+": "+msg)
        print(tokens[index:index+2])
        exit()
        raise Exception(msg)
