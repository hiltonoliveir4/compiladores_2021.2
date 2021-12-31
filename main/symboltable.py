class Symboltable:
    def __init__(self, *args):
        self.subroutineTable = {}
        self.staticTable = {}
        self.fieldTable = {}

        self.count = {
            'STATIC': 0,
            'ARG':0,
            'FIELD':0,
            'VAR':0
        }

    def getCount(self, kind):
        return self.count[kind]

    def addElement(self, name, _type, kind):
        try:
            index = self.count[kind]
        except KeyError:
            raise Exception("Erro on addElement in set index")
        if(kind in ["ARG","VAR"]):
            self.subroutineTable[name] = [_type, kind, index]   
        elif (kind == "STATIC"):
            self.staticTable[name] = [_type, kind, index]
        else:
            self.fieldTable[name] = [_type, kind, index]
        self.count[kind] += 1
        return index
    
    def clear(self):
        self.subroutineTable.clear()
        self.count["ARG"] = 0
        self.count["VAR"] = 0

    def __getitem__(self, key):
        if(key in self.staticTable):
            return self.staticTable[key]
        elif(key in self.subroutineTable):
            return self.subroutineTable[key]
        elif (key in self.fieldTable):
            return self.fieldTable[key]
        else:
            return False
    
    def get(self, key, default = (None, None, -1)):
        if(self[key]):
            ref = self[key]
        else:
            ref = default
        return ref

