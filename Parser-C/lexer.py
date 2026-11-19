import re
from dataclasses import dataclass

PALABRAS_RESERVADAS = {
    "int", "float", "bool", "void", "if", "else", "while", "do", "for",
    "switch", "case", "default", "break", "continue", "return",
    "cout", "true", "false", "using", "namespace"
}


class ErrorLexico(Exception):
    pass

@dataclass
class Token:
    tipo: str
    valor: str
    linea: int
    col: int

ESPECIFICACION = [
    ("COMENTARIO", r"//[^\n]*"),
    ("INCLUDE", r"\#include[ \t]*<[A-Za-z_][\w./]*>"),
    ("NUEVA_LINEA", r"\n"),
    ("ESPACIO", r"[ \t\r]+"),
    ("NUM_INVALIDO", r"\d+(?:\.\d+){2,}|\d+\.(?!\d)|\d+[A-Za-z_]\w*"),
    ("NUM", r"\d+(?:\.\d+)?"),
    ("ID", r"[A-Za-z_]\w*"),
    ("OP2", r"==|!=|<=|>=|&&|\|\||<<|\+\+|--|\+=|-="),
    ("OP1", r"[+\-*/<>=!(){};:,]"),
    ("ERROR", r"."),
]
PATRON = re.compile("|".join(f"(?P<{n}>{p})" for n, p in ESPECIFICACION))

def tokenizar(texto):
    tokens = []
    linea, inicio_linea = 1, 0
    for m in PATRON.finditer(texto):
        clase, lexema = m.lastgroup, m.group()
        col = m.start() - inicio_linea + 1
        if clase == "NUEVA_LINEA":
            linea += 1
            inicio_linea = m.end()
        elif clase in ("ESPACIO", "COMENTARIO"):
            continue
        elif clase in ("ERROR", "NUM_INVALIDO"):
            motivo = "literal numérico mal formado" if clase == "NUM_INVALIDO" else "carácter no reconocido"
            raise ErrorLexico(f"Línea {linea}, col {col}: {motivo} {lexema!r}")
        elif clase == "ID":
            tokens.append(Token(lexema if lexema in PALABRAS_RESERVADAS else "ID", lexema, linea, col))
        elif clase in ("INCLUDE", "NUM"):
            tokens.append(Token(clase, lexema, linea, col))
        else:
            tokens.append(Token(lexema, lexema, linea, col))
    tokens.append(Token("EOF", "", linea, len(texto) - inicio_linea + 1))
    return tokens
