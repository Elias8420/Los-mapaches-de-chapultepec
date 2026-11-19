import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lexer import tokenizar, ErrorLexico
from parser import analizar
from semantico import analizar_semantica, ErrorSemantico

class PruebasFase1(unittest.TestCase):
    def valido(self, codigo):
        self.assertTrue(analizar_semantica(analizar(codigo)))

    def invalido(self, codigo, texto):
        with self.assertRaisesRegex(ErrorSemantico, texto):
            analizar_semantica(analizar(codigo))

    def test_tokens_posicion(self):
        ts = tokenizar('int x = 3;\nfloat y = 2.5;')
        self.assertEqual((ts[0].tipo, ts[0].linea, ts[0].col), ('int', 1, 1))
        self.assertEqual((ts[5].tipo, ts[5].linea, ts[5].col), ('float', 2, 1))

    def test_error_caracter(self):
        with self.assertRaisesRegex(ErrorLexico, 'Línea 1, col 1'):
            tokenizar('@')

    def test_error_numero(self):
        with self.assertRaisesRegex(ErrorLexico, 'literal numérico mal formado'):
            tokenizar('12.5.6')

    def test_valido(self):
        self.valido('int main(){ int x = 2; float y = x + 3.5; bool ok = x < 10; if(ok){ x += 1; } return x; }')

    def test_no_declarada(self):
        self.invalido('int main(){ x = 1; return 0; }', 'sin declaración previa')

    def test_redeclaracion(self):
        self.invalido('int main(){ int x; int x; return 0; }', 'redeclaración')

    def test_tipo(self):
        self.invalido('int main(){ int x = true; return 0; }', 'tipos incompatibles')

    def test_ambito(self):
        self.invalido('int main(){ if(true){ int x = 1; } x = 2; return 0; }', 'sin declaración previa')

    def test_sombreado(self):
        self.valido('int main(){ int x = 1; { bool x = true; } return x; }')

    def test_for(self):
        self.valido('int main(){ for(int i=0; i<3; i++){ int x=i; } return 0; }')

    def test_while_do(self):
        self.valido('int main(){ int x=0; while(x<2){x++;} do{x++;}while(x<3); return x; }')

    def test_funcion(self):
        self.valido('int doble(int x){return x+x;} int main(){int a=doble(2); return a;}')

    def test_error_funcion(self):
        self.invalido('int main(){int x=noexiste(2); return x;}', 'no declarada')

if __name__ == '__main__':
    unittest.main()
