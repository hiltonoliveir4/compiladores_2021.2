from analisador_lexico import AnalisadorLexico
from symboltable import Symboltable
from vmwriter import Vmwriter


class AnalisadorSintatico:
    def __init__(self):
        self.analisador_lexico = AnalisadorLexico()
        self.st = Symboltable()
        self.vm = Vmwriter()
        self.className = ''


        self.ifLabelNum = 0
        self.whileLabelNum = 0

        self.kindToSeg = {
            "FIELD" : "THIS",
            "ARG" : "ARG",
            "STATIC" : "STATIC",
            "VAR" : "LOCAL"
        }

        self.operador = {
            '+' : 'ADD',
            '-' : 'SUB',
            '&' : 'AND',
            '|' : 'OR',
            '<' : 'LT',
            '>' : 'GT',
            '=' : 'EQ'
        }

    def compilar(self):
        self.compilarClasse()

    def escreverEstado(self, estado, flag):
        if(flag == 1):
            self.analisador_lexico.escrever(1, estado)
        else:
            self.analisador_lexico.escrever(2, estado)

    def compilarClasse(self):
        if(self.analisador_lexico.buscartoken() != "class"):
            raise Exception("Era esperado um identificador class no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.escreverEstado('class', 1)
        self.analisador_lexico.escrever()  # espaço para classe
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.className = self.analisador_lexico.buscartoken()

        self.analisador_lexico.escrever()  # espaço para identificador da classe
        self.analisador_lexico.avancar()

        self.analisador_lexico.escrever()  # abertura de chave da classe

        while(self.analisador_lexico.hatoken()):
            self.analisador_lexico.avancar()

            while(self.analisador_lexico.buscartoken() in ["static", "field"]):
                self.compilarClassVarDec()

            while(self.analisador_lexico.buscartoken() in ["method", "constructor", "function"]):
                self.compilarSubroutineDec()

        self.escreverEstado("class", 2)
        self.vm.close()

    def compilarClassVarDec(self):
        self.escreverEstado('classVarDec', 1)

        self.analisador_lexico.escrever()  # espaço para static ou field
        kind = self.analisador_lexico.buscartoken().upper()
        self.analisador_lexico.avancar()

        self.analisador_lexico.escrever()  # espaço para tipo
        tipo = self.analisador_lexico.buscartoken()
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.st.addElement(self.analisador_lexico.buscartoken(), tipo, kind)

        self.analisador_lexico.escrever()  # espaço identifier
        self.analisador_lexico.avancar()

        while self.analisador_lexico.buscartoken() != ";":
            self.analisador_lexico.escrever()  # espaco para vírgula
            self.analisador_lexico.avancar()

            if(self.analisador_lexico.tipo() != 'identifier'):
                raise Exception("Era esperado um identificador no lugar de {0}".format(
                    self.analisador_lexico.buscartoken()))

            self.st.addElement(self.analisador_lexico.buscartoken(), tipo, kind)

            self.analisador_lexico.escrever()  # espaco para identificador
            self.analisador_lexico.avancar()

        self.analisador_lexico.escrever()
        self.analisador_lexico.avancar()

        self.escreverEstado('classVarDec', 2)

    def compilarSubroutineDec(self):
        self.escreverEstado('subroutineDec', 1)

        self.st.clear()
        subRoutineType = self.analisador_lexico.buscartoken()
        if(subRoutineType == 'method'):
            self.st.addElement("this", self.className, "ARG")

        self.analisador_lexico.escrever()  # espaço para method, construct ou function
        tipo = self.analisador_lexico.buscartoken()
        self.analisador_lexico.avancar()

        self.analisador_lexico.escrever()  # escreve o tipo
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        function_name = "{}.{}".format(self.className, self.analisador_lexico.buscartoken())

        self.analisador_lexico.escrever()  # espaço o identificador
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.buscartoken() != '('):
            raise Exception("Era esperado um ( no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para (
        self.analisador_lexico.avancar()

        self.compilarParameterList()

        if(self.analisador_lexico.buscartoken() != ')'):
            raise Exception("Era esperado um ) no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para )
        self.analisador_lexico.avancar()

        self.compilarSubroutineBody(function_name, tipo)

        self.escreverEstado('subroutineDec', 2)

    def compilarParameterList(self):
        self.escreverEstado('parameterList', 1)

        kind = 'ARG'
        if(self.analisador_lexico.buscartoken() == ')'):
            self.escreverEstado('parameterList', 2)
            return

        tipo = self.analisador_lexico.buscartoken()
        self.analisador_lexico.escrever()  # espaço para tipo
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.st.addElement(self.analisador_lexico.buscartoken(), tipo, kind)
        self.analisador_lexico.escrever()  # espaço para identifier
        self.analisador_lexico.avancar()

        while(self.analisador_lexico.buscartoken() != ')'):
            if(self.analisador_lexico.buscartoken() != ','):
                raise Exception("Era esperado uma , no lugar de {0}".format(
                    self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever()  # espaço para ,
            self.analisador_lexico.avancar()

            tipo = self.analisador_lexico.buscartoken()
            self.analisador_lexico.escrever()  # espaço para tipo
            self.analisador_lexico.avancar()

            if(self.analisador_lexico.tipo() != 'identifier'):
                raise Exception("Era esperado um identificador no lugar de {0}".format(
                    self.analisador_lexico.buscartoken()))

            self.st.addElement(self.analisador_lexico.buscartoken(), tipo, kind)
            self.analisador_lexico.escrever()  # espaço o identificador
            self.analisador_lexico.avancar()

        self.escreverEstado('parameterList', 2)

    def compilarSubroutineBody(self, function_name, tipo):
        self.escreverEstado('subroutineBody', 1)

        if(self.analisador_lexico.buscartoken() != '{'):
            raise Exception(
                "Era esperado um" + " { " + "no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para {
        self.analisador_lexico.avancar()

        while(self.analisador_lexico.buscartoken() == 'var'):
            self.compilarVarDec()

        nlocals = self.st.getCount('VAR')
        self.vm.writeFunction(function_name, nlocals)

        if(tipo == 'constructor'):
            self.vm.push("CONST", self.st.getCount("FIELD"))
            self.vm.writeCall("Memory.alloc", 1)
            self.vm.pop('POINTER', 0)
        elif(tipo == 'method'):
            self.vm.push("ARG",0)
            self.vm.pop("POINTER", 0)

        if (self.analisador_lexico.buscartoken() in ["return", "let", "do", "if", "while"]):
            self.compilarStatements()

        if(self.analisador_lexico.buscartoken() != '}'):
            raise Exception("Era esperado um" + " } " +
                            "no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para }
        self.analisador_lexico.avancar()

        self.escreverEstado('subroutineBody', 2)

    def compilarVarDec(self):
        self.escreverEstado('varDec', 1)
        if(self.analisador_lexico.buscartoken() != 'var'):
            raise Exception(
                "Era esperado var no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        kind = 'VAR'
        self.analisador_lexico.escrever()  # espaço para var
        self.analisador_lexico.avancar()

        tipo = self.analisador_lexico.buscartoken()
        self.analisador_lexico.escrever()  # espaço para tipo
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.st.addElement(self.analisador_lexico.buscartoken(), tipo, kind)
        self.analisador_lexico.escrever()  # espaço para identificador
        self.analisador_lexico.avancar()

        while (self.analisador_lexico.buscartoken() == ','):
            if(self.analisador_lexico.buscartoken() != ','):
                raise Exception(
                    "Era esperado , no lugar de {0}".format(self.analisador_lexico.buscartoken()))
            self.analisador_lexico.escrever()  # espaço para ,
            self.analisador_lexico.avancar()

            if(self.analisador_lexico.tipo() != 'identifier'):
                        raise Exception("Era esperado um identificador no lugar de {0}".format(
                            self.analisador_lexico.buscartoken()))

            self.st.addElement(self.analisador_lexico.buscartoken(), tipo, kind)
            self.analisador_lexico.escrever()  # espaço para identificador
            self.analisador_lexico.avancar()

        if(self.analisador_lexico.buscartoken() != ';'):
            raise Exception(
                "Era esperado ; no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para ;
        self.analisador_lexico.avancar()

        self.escreverEstado('varDec', 2)

    def compilarStatements(self):
        self.escreverEstado('statements', 1)

        while (self.analisador_lexico.buscartoken() in ["return", "let", "do", "if", "while"]):
            if(self.analisador_lexico.buscartoken() == "if"):
                self.ifStatement()
            elif(self.analisador_lexico.buscartoken() == "do"):
                self.doStatement()
            elif(self.analisador_lexico.buscartoken() == "let"):
                self.letStatement()
            elif(self.analisador_lexico.buscartoken() == "while"):
                self.whileStatement()
            elif(self.analisador_lexico.buscartoken() == "return"):
                self.returnStatement()
            else:
                while(self.analisador_lexico.buscartoken() != '}'):
                    self.analisador_lexico.escrever()
                    self.analisador_lexico.avancar()

        self.escreverEstado('statements', 2)

    def returnStatement(self):
        self.escreverEstado('returnStatement', 1)
        self.analisador_lexico.escrever()  # espaço para return
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.buscartoken() != ';'):
            self.compilarExpression()

        self.vm.push('CONST', 0)
        self.vm.writeReturn()

        self.analisador_lexico.escrever()  # espaço para ;
        self.analisador_lexico.avancar()

        self.escreverEstado('returnStatement', 2)

    def ifStatement(self):
        self.escreverEstado('ifStatement', 1)

        labelTrue = "IF_TRUE{}".format(self.ifLabelNum)
        labelFalse = "IF_FALSE{}".format(self.ifLabelNum)
        labelEnd = "IF_END{}".format(self.ifLabelNum)

        self.ifLabelNum += 1


        self.analisador_lexico.escrever()  # espaço para if
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.buscartoken() != '('):
            raise Exception("Era esperado um ( no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para (
        self.analisador_lexico.avancar()

        self.compilarExpression()

        self.vm.writeIfGoto(labelTrue)
        self.vm.writeGoto(labelFalse)
        self.vm.writeLabel(labelTrue)

        if(self.analisador_lexico.buscartoken() != ')'):
            raise Exception("Era esperado um ) no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para )
        self.analisador_lexico.avancar()
        
        if(self.analisador_lexico.buscartoken() != '{'):
            raise Exception(
                "Era esperado um " + "{" + " no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para {
        self.analisador_lexico.avancar()

        self.compilarStatements()

        if(self.analisador_lexico.buscartoken() != '}'):
            raise Exception(
                "Era esperado um " + "}" + " no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para }
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.buscartoken() == 'else'):
            self.analisador_lexico.escrever()  # espaço para else
            self.analisador_lexico.avancar()

            if(self.analisador_lexico.buscartoken() != '{'):
                raise Exception(
                    "Era esperado um " + "{" + " no lugar de {0}".format(self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever()  # espaço para {
            self.analisador_lexico.avancar()

            self.compilarStatements()

            if(self.analisador_lexico.buscartoken() != '}'):
                raise Exception(
                    "Era esperado um " + "}" + " no lugar de {0}".format(self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever()  # espaço para }
            self.analisador_lexico.avancar()

            self.vm.writeLabel(labelEnd)

        self.escreverEstado('ifStatement', 2)

    def doStatement(self):
        self.escreverEstado('doStatement', 1)
        self.analisador_lexico.escrever()  # escreve do
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Esperando por um identificador, mas um {} dado " .format(
                self.analisador_lexico.tipo()))

        self.analisador_lexico.escrever()  # escreve o identificador
        ident = self.analisador_lexico.buscartoken()
        self.analisador_lexico.avancar()

        self.compilarSubroutineCall(ident)

        self.vm.pop("TEMP", 0)

        self.analisador_lexico.escrever()
        self.analisador_lexico.avancar()

        self.escreverEstado('doStatement', 2)

    def letStatement(self):
        self.escreverEstado('letStatement', 1)
        array = False

        self.analisador_lexico.escrever()  # escreve  let
        self.analisador_lexico.avancar()

        if (self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Esperando por um identificador no lugar de {}" .format(
                self.analisador_lexico.buscartoken()))

        tipo, categ, pos = self.st.get(self.analisador_lexico.buscartoken())
        categoria = self.kindToSeg[categ]

        self.analisador_lexico.escrever() # escreve o identificador
        self.analisador_lexico.avancar()  
        

        while(self.analisador_lexico.buscartoken() == '['):
            self.analisador_lexico.escrever()  # escreve [
            self.analisador_lexico.avancar()

            self.compilarExpression()

            if (self.analisador_lexico.buscartoken() != ']'):
                raise Exception("Esperando por um ] no lugar de {}" .format(
                    self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever()  # escreve ]
            self.analisador_lexico.avancar()

            self.vm.push(categoria, pos)
            self.vm.writeExpression("ADD")
            self.vm.pop("TEMP", 0)
            array = True

        if (self.analisador_lexico.buscartoken() != '='):
            raise Exception("Esperando por um = no lugar de {}" .format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # escreve =
        self.analisador_lexico.avancar()

        self.compilarExpression()

        if(array):
            self.vm.push("TEMP", 0)
            self.vm.pop("POINTER", 1)
            self.vm.pop("THAT", 0)
        else:
            self.vm.pop(categoria, pos)

        if (self.analisador_lexico.buscartoken() != ';'):
            raise Exception("Esperando por um ; no lugar de {}" .format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # escreve ;
        self.analisador_lexico.avancar()

        self.escreverEstado('letStatement', 2)

    def whileStatement(self):
        self.escreverEstado('whileStatement', 1)

        self.analisador_lexico.escrever()  # escreve while
        self.analisador_lexico.avancar()

        labelTrue = "WHILE_EXP{}".format(self.whileLabelNum)
        labelFalse = "WHILE_END{}".format(self.whileLabelNum)
        self.whileLabelNum += 1
        self.vm.writeLabel(labelTrue)
        if(self.analisador_lexico.buscartoken() != '('):
            raise Exception("Era esperado um ( no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # escreve (
        self.analisador_lexico.avancar()

        self.compilarExpression()
        self.vm.writeExpression("NOT")

        if(self.analisador_lexico.buscartoken() != ')'):
            raise Exception("Era esperado um ) no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # )
        self.analisador_lexico.avancar()

        
        if(self.analisador_lexico.buscartoken() != '{'):
            raise Exception("Era esperado um" + "{" + "no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # {
        self.analisador_lexico.avancar()

        self.vm.writeIfGoto(labelFalse)

        self.compilarStatements()

        self.vm.writeGoto(labelTrue)
        self.vm.writeLabel(labelFalse)

        if(self.analisador_lexico.buscartoken() != '}'):
            raise Exception("Era esperado um" + "}" + "no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # }
        self.analisador_lexico.avancar()

        self.escreverEstado('whileStatement', 2)

    def compilarSubroutineCall(self, ident):
        self.escreverEstado('subroutineCall', 1)
        numargs = 0

        if(self.analisador_lexico.buscartoken() == "."):  # é um método
            self.analisador_lexico.escrever()  # .
            self.analisador_lexico.avancar()
            if(self.analisador_lexico.tipo() != "identifier"):
                raise Exception("Era esperado um identificador no lugar de {0}".format(
                    self.analisador_lexico.buscartoken()))
            subroutine_name = self.analisador_lexico.buscartoken()
            self.analisador_lexico.escrever()  # escreve o identificador
            self.analisador_lexico.avancar()

            type, category, pos = self.st.get(ident)

            if(type != None):
                categoria = self.kindToSeg[category]
                self.vm.push(categoria, pos)
                function_name = "{}.{}".format(type, subroutine_name)
                numargs += 1
            else:
                function_name = "{}.{}".format(ident, subroutine_name)

        elif(self.analisador_lexico.buscartoken() == "("):
            subroutine_name = ident
            function_name = "{}.{}".format(self.className, subroutine_name)
            numargs += 1
            self.vm.push("POINTER", 0)

        if(self.analisador_lexico.buscartoken() != "("):
            raise Exception("Era esperado um ( no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # escreve o (
        self.analisador_lexico.avancar()

        # screver os parametros
        self.compilarExpressionList()

        if(self.analisador_lexico.buscartoken() != ")"):
            raise Exception("Era esperado um ) no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # escreve o )
        self.analisador_lexico.avancar()

        self.vm.writeCall(function_name, numargs)

        self.escreverEstado('subroutineCall', 2)

    def compilarExpressionList(self):
        self.escreverEstado('expressionList', 1)

        numArgs = 0

        if(self.analisador_lexico.buscartoken() == ")"):
            return numArgs

        self.compilarExpression()
        numArgs = numArgs + 1

        while(self.analisador_lexico.buscartoken() != ")"):
            if(self.analisador_lexico.buscartoken() != ","):
                raise Exception("Era esperado um , no lugar de {0}".format(
                    self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever()  # escreve ,
            self.analisador_lexico.avancar()

            self.compilarExpression()

        self.escreverEstado('expressionList', 2)
        return numArgs

    def compilarExpression(self):
        self.escreverEstado('expression', 1)

        self.compilarTermo()

        while (self.analisador_lexico.buscartoken() in ['+', '-', '>', '/', '*', '|', '<', '&', '=']):
            operacao = self.analisador_lexico.buscartoken()
            self.analisador_lexico.escrever()  # escreve +, &amp, |, &lt, &gt, =
            self.analisador_lexico.avancar()

            self.compilarTermo()

            if(operacao in self.operador):
                self.vm.writeExpression(self.operador.get(operacao))
            elif(operacao == "*"):
                self.vm.writeCall("Math.multiply",2)
            elif(operacao == "/"):
                self.vm.writeCall("Math.divide",2)
            else:
                raise Exception
                        
        self.escreverEstado('expression', 2)

    def compilarTermo(self):
        self.escreverEstado('term', 1)

        if(self.analisador_lexico.tipo() == 'integer'):
            self.vm.push('CONST', int(self.analisador_lexico.buscartoken()))
            self.analisador_lexico.escrever()
            self.analisador_lexico.avancar()

        elif(self.analisador_lexico.tipo() == 'string'):
            self.compilarString()

        elif(self.analisador_lexico.buscartoken() in ['false', 'true', 'null']):
            self.vm.push('CONST', 0)
            if(self.analisador_lexico.buscartoken() == 'true'):
                self.vm.writeExpression('NOT')
            self.analisador_lexico.escrever()
            self.analisador_lexico.avancar()

        elif(self.analisador_lexico.buscartoken() == 'this'):
            self.vm.push("POINTER", 0)
            self.analisador_lexico.escrever()
            self.analisador_lexico.avancar()      

        elif(self.analisador_lexico.tipo() == 'identifier'):
            ident = self.analisador_lexico.buscartoken()
            self.analisador_lexico.escrever()  # escreve o identificador
            self.analisador_lexico.avancar()

            if (self.analisador_lexico.buscartoken() in ['(', '.']):
                self.compilarSubroutineCall(ident)

            else: #array
                if (self.analisador_lexico.buscartoken() == '['):
                    self.analisador_lexico.escrever()  # escreve o [
                    self.analisador_lexico.avancar()

                    self.compilarExpression()

                    tipo, categ, pos = self.st.get(ident)
                    category = self.kindToSeg[categ]
                    self.vm.push(category, pos)
                    self.vm.writeExpression("ADD")

                    if(self.analisador_lexico.buscartoken() != "]"):
                        raise Exception("Era esperado um } no lugar de {0}".format(
                            self.analisador_lexico.buscartoken()))
                    
                    self.vm.pop("POINTER", 1)
                    self.vm.push("THAT", 0)

                    self.analisador_lexico.escrever()  # escreve o ]
                    self.analisador_lexico.avancar()
                
                else: #variavel simples
                    tipo, categ, pos = self.st.get(ident)
                    category = self.kindToSeg[categ]
                    self.vm.push(category, pos)

        elif(self.analisador_lexico.buscartoken() == '('):
            self.analisador_lexico.escrever()  # escreve o (
            self.analisador_lexico.avancar()

            self.compilarExpression()

            if(self.analisador_lexico.buscartoken() != ")"):
                raise Exception("Era esperado um ) no lugar de {0}".format(
                    self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever()  # escreve o )
            self.analisador_lexico.avancar()

        elif(self.analisador_lexico.buscartoken() in ['-', '~']):
            self.analisador_lexico.escrever()  # escreve - ou ~
            self.analisador_lexico.avancar()

            op = self.analisador_lexico.buscartoken()
            self.compilarTermo()

            if(op == "-"):
                self.vm.writeExpression("NEG")
            else:
                self.vm.writeExpression("NOT")

        else:
            raise Exception("Era esperado um termo no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.escreverEstado('term', 2)

    def compilarString(self):
        self.escreverEstado('stringStatement',1)
        string = self.analisador_lexico.buscartoken()

        self.vm.push("CONST", len(string))
        self.vm.writeCall("String.new", 1)

        for char in string:
            self.vm.push("CONST", ord(char))
            self.vm.writeCall("String.appendChar", 2)

        self.analisador_lexico.escrever()
        self.analisador_lexico.avancar()

        self.escreverEstado('stringStatement', 2)

a = AnalisadorSintatico()
a.compilar()
