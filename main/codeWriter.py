class CodeWriter:

    def __init__(self, path):
        self.output = open("./projects/"+path+".vm", "w+")

    def write(self, valor):
        self.output.writelines("{}\n".format(valor))

    # def writeInit(self):
    #   self.write("@256")
    #   self.write("D=A")

    def segmentPointer(self, seg, index):
        if seg == "local":
            return "LCL"
        elif seg == "argument":
            return "ARG"
        elif seg == "this":
            return "THIS"
        elif seg == "that":
            return "THAT"
        elif seg == "temp":
            return self.output.writelines("R{}\n".format(5+index))
        elif seg == "pointer":
            return self.output.writelines("R{}\n".format(3+index))
        elif seg == "static":
            return self.output.writelines("{}".format(index))
        else:
            return "ERROR"

    def writePush(self, segment, index):
        if segment == "constant":
            self.write(self.output.writelines(
                "{} //" + " push {} {}" .format(index, segment, index)))
            self.write("D=A")
            self.write("@SP")
            self.write("A=M")
            self.write("M=D")
            self.write("@SP")
            self.write("M = M + 1")
        elif segment == "static" or segment == "temp" or segment == "pointer":
            self.write(self.output.writelines(
                "{} //" + " push {} {}" .format(self.segmentPointer(segment, index), segment, index)))
            self.write("D=M")
            self.write("@SP")
            self.write("A=M")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M+1")
        elif segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            self.write(self.output.writelines(
                "{} //" + " push {} {}" .format(self.segmentPointer(segment, index), segment, index)))
            self.write("D=M")
            self.write(self.output.writelines("{}" .format(index)))
            self.write("A=D+A")
            self.write("D=M")
            self.write("@SP")
            self.write("A=M")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M+1")

    def writePop(self, segment, index):
        if segment == "static" or segment == "temp" or segment == "pointer":
            self.write(self.output.writelines(
                "@SP //" + " pop {} {}" .format(segment, index)))
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write(self.output.writelines(
                "{}" .format(self.segmentPointer(segment, index))))
            self.write("M=D")
        elif segment == "local" or segment == "argument" or segment == "this" or segment == "that":
            self.write(self.output.writelines(
                "{} //" + " pop {} {}" .format(self.segmentPointer(segment, index), segment, index)))
            self.write("D=M")
            self.write(self.output.writelines("{}" .format(index)))
            self.write("D=D+A")
            self.write("@R13")
            self.write("M=D")
            self.write("@SP")
            self.write("M=M-1")
            self.write("A=M")
            self.write("D=M")
            self.write("@R13")
            self.write("A=M")
            self.write("M=D")

    def writeArithmetic(self, cmd):
        if cmd.Name == "add":
            self.writeArithmeticAdd()
        elif cmd.Name == "sub":
            self.writeArithmeticSub()
        elif cmd.Name == "neg":
            self.writeArithmeticNeg()
        elif cmd.Name == "eq":
            self.writeArithmeticEq()
        elif cmd.Name == "gt":
            self.writeArithmeticGt()
        elif cmd.Name == "lt":
            self.writeArithmeticLt()
        elif cmd.Name == "and":
            self.writeArithmeticAnd()
        elif cmd.Name == "or":
            self.writeArithmeticOr()
        elif cmd.Name == "not":
            self.writeArithmeticNot()

    def writeBinaryArithmetic(self):
        self.write("@SP")
        self.write("AM=M-1")
        self.write("D=M")
        self.write("A=A-1")

    def writeArithmeticAdd(self):
        self.writeBinaryArithmetic()
        self.write("M=D+M")

    def writeArithmeticSub(self):
        self.writeBinaryArithmetic()
        self.write("M=M-D")

    def writeArithmeticAnd(self):
        self.writeBinaryArithmetic()
        self.write("M=D&M")

    def writeArithmeticOr(self):
        self.writeBinaryArithmetic()
        self.write("M=D|M")

    def writeUnaryArithmetic(self):
        self.write("@SP")
        self.write("A=M")
        self.write("A=A-1")

    def writeArithmeticNeg(self):
        self.writeUnaryArithmetic()
        self.write("M=-M")

    def writeArithmeticNot(self):
        self.writeUnaryArithmetic()
        self.write("M=!M")

    def writeArithmeticEq(self):
        returnAddr = self.output.writelines(
            "$RET{}" .format(self.returnSubCount))
        self.write(self.output.writelines("@{}" .format(self.returnAddr)))
        self.write("D=A")
        self.write("@EQ$")
        self.write("0;JMP")
        self.write(self.output.writelines("{}" .format(self.returnAddr)))
        self.returnSubCount = self.returnSubCount + 1

    def writeArithmeticGt(self):
        returnAddr = self.output.writelines(
            "$RET{}" .format(self.returnSubCount))
        self.write(self.output.writelines("@{}" .format(self.returnAddr)))
        self.write("D=A")
        self.write("@$GT$")
        self.write("0;JMP")
        self.write(self.output.writelines("{}" .format(self.returnAddr)))
        self.returnSubCount = self.returnSubCount + 1

    def writeArithmeticLt(self):
        returnAddr = self.output.writelines(
            "$RET{}" .format(self.returnSubCount))
        self.write(self.output.writelines("@{}" .format(self.returnAddr)))
        self.write("D=A")
        self.write("@$LT$")
        self.write("0;JMP")
        self.write(self.output.writelines("{}" .format(self.returnAddr)))
        self.returnSubCount = self.returnSubCount + 1

    def writeClose(self):
        self.output.Close()
