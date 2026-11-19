import sys
from lexer import tokenizar, ErrorLexico
from parser import analizar, ErrorSintactico
from semantico import analizar_semantica, ErrorSemantico

def ejecutar(codigo, mostrar_tokens=False, mostrar_arbol=False):
    try:
        if mostrar_tokens:
            for tok in tokenizar(codigo):
                print(tok)
        arbol = analizar(codigo)
        if mostrar_arbol:
            arbol.imprimir()
        analizar_semantica(arbol)
        print('OK: análisis léxico, sintáctico y semántico completados')
        return True
    except (ErrorLexico, ErrorSintactico, ErrorSemantico) as error:
        print(f'ERROR: {error}')
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python ejecutar.py archivo.cpp [--tokens] [--arbol]')
        sys.exit(2)
    with open(sys.argv[1], encoding='utf-8') as f:
        codigo = f.read()
    sys.exit(0 if ejecutar(codigo, '--tokens' in sys.argv, '--arbol' in sys.argv) else 1)
