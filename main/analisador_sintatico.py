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
        self.analisador_lexico.escrever() #espaço para classe
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(self.analisador_lexico.buscartoken()))
        
        self.analisador_lexico.escrever() #espaço para identificador da classe
        self.analisador_lexico.avancar()

        self.analisador_lexico.escrever() #abertura de chave da classe

        while(self.analisador_lexico.hatoken()):
            self.analisador_lexico.avancar()

            while(self.analisador_lexico.buscartoken() in ["static", "field"]):
                self.compilarClassVarDec()
            
            while(self.analisador_lexico.buscartoken() in ["method", "constructor", "function"]):
                self.compilarSubroutineDec()

        self.escreverEstado("class", 2)

    def compilarClassVarDec(self):
        self.escreverEstado('classVarDec',1)

        self.analisador_lexico.escrever() #espaço para static ou field
        self.analisador_lexico.avancar() 
        self.analisador_lexico.escrever() #espaço para tipo
        self.analisador_lexico.avancar() 

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever() #espaço identifier
        self.analisador_lexico.avancar()

        while self.analisador_lexico.buscartoken() != ";":
            self.analisador_lexico.escrever() #espaco para vírgula
            self.analisador_lexico.avancar()

            if(self.analisador_lexico.tipo() != 'identifier'):
                raise Exception("Era esperado um identificador no lugar de {0}".format(self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever() #espaco para identificador
            self.analisador_lexico.avancar() 

        self.analisador_lexico.escrever()
        self.analisador_lexico.avancar()

        self.escreverEstado('classVarDec',2)

    def compilarSubroutineDec(self):
        self.escreverEstado('subroutineDec',1)
        
        self.analisador_lexico.escrever() #espaço para method, construct ou function
        self.analisador_lexico.avancar()

        self.analisador_lexico.escrever() #escreve o tipo
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever() #espaço o identificador
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.buscartoken() != '('):
            raise Exception("Era esperado um ( no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever() #espaço para (
        self.analisador_lexico.avancar()

        self.compilarParameterList()

        if(self.analisador_lexico.buscartoken() != ')'):
            raise Exception("Era esperado um ) no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever() #espaço para )
        self.analisador_lexico.avancar()

        self.compilarSubroutineBody()

        self.escreverEstado('subroutineDec',2)

    def compilarParameterList(self):
        self.escreverEstado('parameterList',1)

        if(self.analisador_lexico.buscartoken() == ')'):
            self.escreverEstado('parameterList',2)
            return
        
        self.analisador_lexico.escrever() #espaço para tipo
        self.analisador_lexico.avancar()
        
        if(self.analisador_lexico.tipo() != 'identifier'):
            raise Exception("Era esperado um identificador no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever() #espaço para identifier
        self.analisador_lexico.avancar()

        while(self.analisador_lexico.buscartoken() != ')'):
            if(self.analisador_lexico.buscartoken() != ','):
                raise Exception("Era esperado uma , no lugar de {0}".format(self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever() #espaço para ,
            self.analisador_lexico.avancar()
            self.analisador_lexico.escrever() #espaço para tipo
            self.analisador_lexico.avancar()

            if(self.analisador_lexico.tipo() != 'identifier'):
                raise Exception("Era esperado um identificador no lugar de {0}".format(self.analisador_lexico.buscartoken()))

            self.analisador_lexico.escrever() #espaço o identificador
            self.analisador_lexico.avancar()

        self.escreverEstado('parameterList',2)

    def compilarSubroutineBody(self):
        self.escreverEstado('subroutineBody',1)

        if(self.analisador_lexico.buscartoken() != '{'):
            raise Exception("Era esperado um" + " { " + "no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever() #espaço para {
        self.analisador_lexico.avancar()
        
        if (self.analisador_lexico.buscartoken() in ["return", "let", "do", "if", "while"]):
            self.compilarStatements()

        if(self.analisador_lexico.buscartoken() != '}'):
            raise Exception("Era esperado um" + " } " + "no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever() #espaço para }
        self.analisador_lexico.avancar()

        self.escreverEstado('subroutineBody',2)

    def compilarStatements(self):
        self.escreverEstado('statements',1)

        while (self.analisador_lexico.buscartoken() in ["return", "let", "do", "if", "while"]):
            if(self.analisador_lexico.buscartoken() == "if"):
                self.ifStatement()
            else:
                while(self.analisador_lexico.buscartoken() != '}'):
                    self.analisador_lexico.escrever()
                    self.analisador_lexico.avancar()
            # elif(self.analisador_lexico.buscartoken == "do"):
            #     self.doStatement()
            # elif(self.analisador_lexico.buscartoken == "let"):
            #     self.letStatement()
            # elif(self.analisador_lexico.buscartoken == "while"):
            #     self.whileStatement()
            # elif(self.analisador_lexico.buscartoken == "return"):
            #     self.returnStatement()

        self.escreverEstado('statements',2)

    def ifStatement(self):
        self.escreverEstado('ifStatement',1)

        self.analisador_lexico.escrever() #espaço para if
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.buscartoken() != '('):
            raise Exception("Era esperado um ( no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever() #espaço para (
        self.analisador_lexico.avancar()

        # self.compilarExpression() ################################################
        while(self.analisador_lexico.buscartoken() != ')'):
            self.analisador_lexico.escrever()
            self.analisador_lexico.avancar()

        self.analisador_lexico.escrever() #espaço para )
        self.analisador_lexico.avancar()

        if(self.analisador_lexico.buscartoken() != '{'):
            raise Exception("Era esperado um " + "{" + " no lugar de {0}".format(self.analisador_lexico.buscartoken()))

        self.analisador_lexico.escrever() #espaço para {
        self.analisador_lexico.avancar()

        self.compilarStatements()

        self.analisador_lexico.escrever() #espaço para }
        self.analisador_lexico.avancar()

        #tem else nesse negocio????

        self.escreverEstado('ifStatement',2)

a = AnalisadorSintatico()
a.compilar()