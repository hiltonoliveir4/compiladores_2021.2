import re

class AnalisadorLexico:
    regex = re.compile('".*"|[0-9]+|[a-zA-Z_]+[a-zA-Z0-9_]*|[+|*|/|\-|{|}|(|)|\[|\]|\.|,|;|<|>|=|~|&]')
    keyword = [
        'class','constructor','function','method','field','static',
        'var' ,'int','char','boolean' ,'void' ,'true','false','null',
        'this','let','do','if','else','while','return'
    ]
    symbol = '[+|*|/|{|}|(|)|.|,|;|<|>|=|~]'
    identifier = '[a-zA-Z_]+[a-zA-Z0-9_]*'
    integer = '[0-9]+'
    string = '".*"'

    def __init__(self):
        self.arquivo = open('main.txt', 'r').read()
        self.arquivo = re.sub('//.*'," ", self.arquivo) #remover os comentário com //
        self.arquivo = re.sub('(/\*(.|\n)*?\*/)'," ", self.arquivo) #remover os comentário com /* */
        self.tokens = self.regex.findall(self.arquivo)

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

        elif(re.match(self.integer, token)):
            return 'integer'
        
        elif(re.match(self.string, token)):
            return 'string'

    def escrever(self):
        saida = open('saida.xml', 'w+')
        saida.writelines('<tokens>\n') 
        for token in self.tokens:
            tipo = self.tipo(token)

            saida.writelines(('<{0}> {1} </{2}>\n'.format(tipo, token, tipo)))
        saida.writelines('</tokens>') 
        print('finalizado')

analisador = AnalisadorLexico()
analisador.escrever()
