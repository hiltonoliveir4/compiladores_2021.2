class Vmwriter:

    def __init__(self):
        self.output = open("./main/square.vm", "w+")

        self.helperDict = {
            "POINTER": "pointer",
            "LOCAL":"local",
            "THAT":"that",
            "THIS":"this",
            "TEMP":"temp",
            "STATIC":"static",
            "ARG":"argument",
            "CONST":"constant",
            "FIELD":"this"
        }

    def pop(self, segment, index):
        replaced = self.helperDict.get(segment)

        if(replaced == None):
            raise Exception("Error 1")
        self.output.writelines("pop {} {}\n".format(replaced, index))
    
    def push(self, segment, index):

        replaced = self.helperDict.get(segment)
        if(replaced == None):
            return Exception
        self.output.writelines("push {} {}\n".format(replaced, index))
        
    def writeReturn(self):
        self.output.writelines("return\n")
    
    def writeGoto(self, label):
        self.output.writelines("goto {}\n".format(label))

    def writeIfGoto(self, label):
        self.output.writelines("if-goto {}".format(label))
    
    def writeLabel(self, label):
        self.output.writelines("label {}\n".format(label))
    
    def writeCall(self, name, len_args):
        self.output.writelines("call {} {}\n".format(name, len_args))

    def writeFunction(self, name, len_local):
        self.output.writelines("function {} {}\n".format(name, len_local))
    
    def writeExpression(self, command):
        if(command not in ["ADD", "SUB", "NEG", "EQ", "GT", "LT", "AND", "OR", "NOT"]):
            raise Exception
        localCase = command.lower()
        self.output.writelines(localCase + '\n')
    
    def close(self):
        self.output.writelines("close \n")

