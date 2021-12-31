from analisador_sintatico import AnalisadorSintatico

arquivos = [
    'Average/average',
    'ComplexArrays/Main',
    'ConvertToBin/Main',
    'Pong/Ball',
    'Pong/Bat',
    'Pong/Main',
    'Pong/PongGame',
    'Seven/Main',
    'Square/Main',
    'Square/Square',
    'Square/SquareGame',
]

for arquivo in arquivos:
    a = AnalisadorSintatico(arquivo)
    a.compilar()

