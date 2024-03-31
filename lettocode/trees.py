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
