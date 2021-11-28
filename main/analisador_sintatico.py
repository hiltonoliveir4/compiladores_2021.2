from analisador_lexico import AnalisadorLexico
import re


class AnalisadorSintatico:
    def __init__(self):
        self.analisador_lexico = AnalisadorLexico()

    def compilar(self):
        self.compilarClasse()

    def escreverEstado(self, estado, flag):
        if(flag == 1):
            self.analisador_lexico.escrever(1, estado)
        else:
            self.analisador_lexico.escrever(2, estado)

    def compilarClasse(self):
        if(self.analisador_lexico.buscartoken() != "class"):
            print('ERROR: Um keyword class era esperado')
            return

        self.escreverEstado('class', 1)
        self.analisador_lexico.escrever()  # espaço para classe
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

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

    def compilarClassVarDec(self):
        self.escreverEstado('classVarDec', 1)

        self.analisador_lexico.escrever()  # espaço para static ou field
        self.analisador_lexico.avancar()
        self.analisador_lexico.escrever()  # espaço para tipo
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço identifier
        self.analisador_lexico.avancar()

        while self.analisador_lexico.buscartoken() != ";":
            self.analisador_lexico.escrever()  # espaco para vírgula
            self.analisador_lexico.avancar()

            if(self.analisador_lexico.tipo() != 'identifier'):
                raise Exception("Era esperado um identificador no lugar de {0}".format(
                    self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever()  # espaco para identificador
            self.analisador_lexico.avancar()

        self.analisador_lexico.escrever()
        self.analisador_lexico.avancar()

        self.escreverEstado('classVarDec', 2)

    def compilarSubroutineDec(self):
        self.escreverEstado('subroutineDec', 1)

        self.analisador_lexico.escrever()  # espaço para method, construct ou function
        self.analisador_lexico.avancar()

        self.analisador_lexico.escrever()  # escreve o tipo
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

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

        self.compilarSubroutineBody()

        self.escreverEstado('subroutineDec', 2)

    def compilarParameterList(self):
        self.escreverEstado('parameterList', 1)

        if(self.analisador_lexico.buscartoken() == ')'):
            self.escreverEstado('parameterList', 2)
            return

        self.analisador_lexico.escrever()  # espaço para tipo
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para identifier
        self.analisador_lexico.avancar()

        while(self.analisador_lexico.buscartoken() != ')'):
            if(self.analisador_lexico.buscartoken() != ','):
                raise Exception("Era esperado uma , no lugar de {0}".format(
                    self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever()  # espaço para ,
            self.analisador_lexico.avancar()
            self.analisador_lexico.escrever()  # espaço para tipo
            self.analisador_lexico.avancar()

            if(self.analisador_lexico.tipo() != 'identifier'):
                raise Exception("Era esperado um identificador no lugar de {0}".format(
                    self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever()  # espaço o identificador
            self.analisador_lexico.avancar()

        self.escreverEstado('parameterList', 2)

    def compilarSubroutineBody(self):
        self.escreverEstado('subroutineBody', 1)

        if(self.analisador_lexico.buscartoken() != '{'):
            raise Exception(
                "Era esperado um" + " { " + "no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para {
        self.analisador_lexico.avancar()

        if (self.analisador_lexico.buscartoken() in ["return", "let", "do", "if", "while"]):
            self.compilarStatements()

        if(self.analisador_lexico.buscartoken() != '}'):
            raise Exception("Era esperado um" + " } " +
                            "no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para }
        self.analisador_lexico.avancar()

        self.escreverEstado('subroutineBody', 2)

    def compilarStatements(self):
        self.escreverEstado('statements', 1)

        while (self.analisador_lexico.buscartoken() in ["return", "let", "do", "if", "while"]):
            if(self.analisador_lexico.buscartoken() == "if"):
                self.ifStatement()
            elif(self.analisador_lexico.buscartoken() == "do"):
                self.doStatement()
            elif(self.analisador_lexico.buscartoken == "let"):
                self.letStatement()
            elif(self.analisador_lexico.buscartoken == "while"):
                self.whileStatement()
            elif(self.analisador_lexico.buscartoken == "return"):
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

        self.analisador_lexico.escrever()  # espaço para ;
        self.analisador_lexico.avancar()

        self.escreverEstado('returnStatement', 2)

    def ifStatement(self):
        self.escreverEstado('ifStatement', 1)

        self.analisador_lexico.escrever()  # espaço para if
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.buscartoken() != '('):
            raise Exception("Era esperado um ( no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # espaço para (
        self.analisador_lexico.avancar()

        self.compilarExpression()

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

        self.escreverEstado('ifStatement', 2)

    def doStatement(self):
        self.escreverEstado('doStatement', 1)
        self.analisador_lexico.escrever()  # escreve do
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Esperando por um identificador, mas um {} dado " .format(
                self.analizador_lexico.tipo()))

        self.analisador_lexico.escrever()  # escreve o identificador
        self.analisador_lexico.avancar()

        self.compilarSubroutineCall()

        self.analisador_lexico.escrever()
        self.analisador_lexico.avancar()

        self.escreverEstado('doStatement', 2)

    def letStatement(self):
        self.escreverEstado('letStatement', 1)

        self.analizador_lexico.escrever()  # escreve  let
        self.analizador_lexico.avancar()

        if (self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Esperando por um identificador no lugar de {}" .format(
                self.analizador_lexico.buscartoken()))

        self.analizador_lexico.avancar()  # escreve o identificador
        self.analizador_lexico.escrever()

        while(self.analisador_lexico.buscartoken() == '['):
            self.analizador_lexico.escrever()  # escreve [
            self.analizador_lexico.avancar()

            self.compilarExpression()

            if (self.analisador_lexico.buscartoken() != ']'):
                raise Exception("Esperando por um ] no lugar de {}" .format(
                    self.analizador_lexico.buscartoken()))

            self.analizador_lexico.escrever()  # escreve ]
            self.analizador_lexico.avancar()

        if (self.analisador_lexico.buscartoken() != '='):
            raise Exception("Esperando por um = no lugar de {}" .format(
                self.analizador_lexico.buscartoken()))

        self.analizador_lexico.escrever()  # escreve =
        self.analizador_lexico.avancar()

        self.compilarExpression()

        if (self.analisador_lexico.buscartoken() != ';'):
            raise Exception("Esperando por um ; no lugar de {}" .format(
                self.analizador_lexico.buscartoken()))

        self.analizador_lexico.escrever()  # escreve ;
        self.analizador_lexico.avancar()

        self.escreverEstado('letStatement', 2)

    def whileStatement(self):
        self.escreverEstado('whileStatement', 1)

        self.analisador_lexico.escrever()  # escreve while
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.buscartoken() != '('):
            raise Exception("Era esperado um ( no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analizador_lexico.escrever()  # escreve (
        self.analizador_lexico.avancar()

        self.compilarExpression()

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

        self.compilarStatements()

        if(self.analisador_lexico.buscartoken() != '}'):
            raise Exception("Era esperado um" + "}" + "no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever()  # }
        self.analisador_lexico.avancar()

        self.escreverEstado('whileStatement', 2)

    def compilarSubroutineCall(self):
        self.escreverEstado('subroutineCall', 1)
        # if(self.analisador_lexico.buscartoken() != "("):
        #     raise Exception("Era esperado um identificador no lugar de {0}".format(
        #         self.analisador_lexico.buscartoken()))

        if(self.analisador_lexico.buscartoken() == "."):  # é um método
            self.analisador_lexico.escrever()  # .
            self.analisador_lexico.avancar()
            if(self.analisador_lexico.tipo() != "identifier"):
                raise Exception("Era esperado um identificador no lugar de {0}".format(
                    self.analisador_lexico.buscartoken()))
            self.analisador_lexico.escrever()  # escreve o identificador
            self.analisador_lexico.avancar()

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

        self.escreverEstado('subroutineCall', 2)

    def compilarExpressionList(self):
        self.escreverEstado('expressionList', 1)

        if(self.analisador_lexico.buscartoken() == ")"):
            return

        self.compilarExpression()

        while(self.analisador_lexico.buscartoken() != ")"):
            if(self.analisador_lexico.buscartoken() != ","):
                raise Exception("Era esperado um , no lugar de {0}".format(
                    self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever()  # escreve ,
            self.analisador_lexico.avancar()

            self.compilarExpression()

        self.escreverEstado('expressionList', 2)

    def compilarExpression(self):
        self.escreverEstado('expression', 1)

        self.compilarTermo()

        while (self.analisador_lexico.buscartoken() in ['+', '-', '&amp', '|', '&lt', '&gt', '=']):
            self.analisador_lexico.escrever()  # escreve +, &amp, |, &lt, &gt, =
            self.analisador_lexico.avancar()

            if(self.analisador_lexico.buscartoken() != ","):
                raise Exception("Era esperado um , no lugar de {0}".format(
                    self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever()  # escreve ,
            self.analisador_lexico.avancar()

            self.compilarTermo()

        self.escreverEstado('expression', 2)

    def compilarTermo(self):
        self.escreverEstado('term', 1)

        if(self.analisador_lexico.tipo() in ['string', 'integer'] or self.analisador_lexico.buscartoken() in ['true', 'false', 'null', 'this']):
            self.analisador_lexico.escrever()
            self.analisador_lexico.avancar()

        elif(self.analisador_lexico.tipo() == 'identifier'):
            self.analisador_lexico.escrever()  # escreve o identificador
            self.analisador_lexico.avancar()

            if(self.analisador_lexico.buscartoken() == '{'):
                self.analisador_lexico.escrever()  # escreve o {
                self.analisador_lexico.avancar()

                self.compilarExpression()

                if(self.analisador_lexico.buscartoken() != "}"):
                    raise Exception("Era esperado um } no lugar de {0}".format(
                        self.analisador_lexico.buscartoken()))

                self.analisador_lexico.escrever()  # escreve o )
                self.analisador_lexico.avancar()

            elif (self.analisador_lexico.buscartoken() in ['(', '.']):
                self.compilarSubroutineCall()

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

            self.compilarTermo()

        else:
            print(self.analisador_lexico.buscartoken())
            print(self.analisador_lexico.indice)
            print(
                self.analisador_lexico.tokens[self.analisador_lexico.indice - 1])
            raise Exception("Era esperado um termo no lugar de {0}".format(
                self.analisador_lexico.buscartoken()))

        self.escreverEstado('term', 2)


a = AnalisadorSintatico()
a.compilar()
