import re

class AnalisadorLexico:
    regex = re.compile('[a-zA-Z_]+[a-zA-Z0-9_]*|[+|*|/|\-|{|}|(|)|\[|\]|\.|,|;|<|>|=|~|&]')

    keyword = [
        'class','constructor','function','method','field','static',
        'var' ,'int','char','boolean' ,'void' ,'true','false','null',
        'this','let','do','if','else','while','return'
    ]

    symbol = '[+|*|/|{|}|(|)|.|,|;|<|>|=|~]'
    identifier = '[a-zA-Z_]+[a-zA-Z0-9_]*'

    def __init__(self, caminho):
        self.arquivo = open('main.txt', 'r').read()
        self.arquivo = re.sub('//.*'," ", self.arquivo)
        self.arquivo = re.sub('(/\*(.|\n)*?\*/)'," ", self.arquivo)
        self.tokens = self.regex.findall(self.arquivo)
        self.saida = open('tokens.xml', 'w+')

    def trocarXML(self, simbolo):
        if (simbolo == '>'):
            return '&gt;'
        if (simbolo == '<'):
            return '&lt;'
        if (simbolo == '&'):
            return '&amp;'
        if (simbolo == '"'):
            return '&quot;'
        else:
            return simbolo

    def tipo(self, token):
        if(re.match(self.identifier, token)):
            if(token in self.keyword):
                return 'keyword'
            else:
                return 'identifier'

        elif(re.match(self.symbol, token)):
            return 'symbol'

    def escrever(self):
        self.saida.writelines('<tokens>\n') 
        for token in self.tokens:
            tipo = self.tipo(token)

            self.saida.writelines(('<{0}> {1} </{2}>\n'.format(tipo, token, tipo)))
        self.saida.writelines('</tokens>') 
        print('finalizado')

analisador = AnalisadorLexico("main.txt")
analisador.escrever()
