"""Análisis semántico del subconjunto C++ definido en parser.py."""

class ErrorSemantico(Exception):
    pass

class AnalizadorSemantico:
    def __init__(self):
        self.ambitos = [{}]
        self.funciones = {}
        self.retorno = None

    def error(self, mensaje, nodo):
        linea = getattr(nodo, 'linea', None)
        col = getattr(nodo, 'col', None)
        ubicacion = f'Línea {linea}, col {col}: ' if linea is not None else 'Ubicación desconocida: '
        raise ErrorSemantico(ubicacion + mensaje)

    def entrar(self):
        self.ambitos.append({})

    def salir(self):
        self.ambitos.pop()

    def declarar(self, nodo, tipo):
        nombre = nodo.valor
        if nombre in self.ambitos[-1]:
            self.error(f"redeclaración de '{nombre}' en el mismo ámbito", nodo)
        self.ambitos[-1][nombre] = tipo

    def buscar(self, nodo):
        for ambito in reversed(self.ambitos):
            if nodo.valor in ambito:
                return ambito[nodo.valor]
        self.error(f"variable '{nodo.valor}' utilizada sin declaración previa", nodo)

    @staticmethod
    def tipo_decl(nodo):
        return nodo.hijos[0].hijos[0].etiqueta

    def compatible(self, destino, origen):
        # En este subconjunto se permite conversión int -> float, no bool -> int.
        return destino == origen or (destino == 'float' and origen == 'int')

    def exigir(self, destino, origen, nodo):
        if not self.compatible(destino, origen):
            self.error(f'tipos incompatibles: se esperaba {destino}, se obtuvo {origen}', nodo)

    def expresion(self, n):
        e, h = n.etiqueta, n.hijos
        if e == 'NUM':
            return 'float' if '.' in n.valor else 'int'
        if e == 'ID':
            return self.buscar(n)
        if e in ('true', 'false'):
            return 'bool'
        if e == 'grupo':
            return self.expresion(h[1])
        if e == 'llamada':
            return self.llamada(n)
        if e == 'unario':
            op, tipo = h[0].etiqueta, self.expresion(h[1])
            if op == '!' and tipo == 'bool':
                return 'bool'
            if op == '-' and tipo in ('int', 'float'):
                return tipo
            self.error(f'operador unario {op} incompatible con {tipo}', h[0])
        if e in ('suma', 'term', 'rel', 'and', 'or'):
            izq, der = self.expresion(h[0]), self.expresion(h[2])
            op = h[1].etiqueta
            if e in ('and', 'or'):
                if izq == der == 'bool':
                    return 'bool'
            elif e in ('suma', 'term'):
                if izq in ('int', 'float') and der in ('int', 'float'):
                    return 'float' if 'float' in (izq, der) or op == '/' else 'int'
            elif e == 'rel':
                if izq in ('int', 'float') and der in ('int', 'float'):
                    return 'bool'
                if op in ('==', '!=') and izq == der == 'bool':
                    return 'bool'
            self.error(f'operación {op} incompatible con {izq} y {der}', h[1])
        self.error(f'expresión no soportada: {e}', n)

    def llamada(self, n):
        nombre = n.hijos[0]
        if nombre.valor not in self.funciones:
            self.error(f"función '{nombre.valor}' no declarada", nombre)
        retorno, parametros = self.funciones[nombre.valor]
        argumentos = [x for x in n.hijos[2].hijos if x.etiqueta != ',']
        if len(argumentos) != len(parametros):
            self.error(f"función '{nombre.valor}' espera {len(parametros)} argumentos, recibió {len(argumentos)}", nombre)
        for arg, esperado in zip(argumentos, parametros):
            self.exigir(esperado, self.expresion(arg), nombre)
        if retorno == 'void':
            self.error('una función void no puede usarse como expresión', nombre)
        return retorno

    def sentencia(self, n):
        e, h = n.etiqueta, n.hijos
        if e == 'bloque':
            self.entrar()
            try:
                for hijo in h[1:-1]:
                    self.sentencia(hijo)
            finally:
                self.salir()
        elif e == 'decl':
            tipo, nombre = self.tipo_decl(n), h[1]
            self.declarar(nombre, tipo)
            if len(h) > 2 and h[2].etiqueta == '=':
                self.exigir(tipo, self.expresion(h[3]), nombre)
        elif e == 'asignacion':
            nombre, op = h[0], h[1].etiqueta
            tipo = self.buscar(nombre)
            if op in ('++', '--'):
                if tipo not in ('int', 'float'):
                    self.error(f'{op} requiere una variable numérica', nombre)
            else:
                nuevo = self.expresion(h[2])
                if op in ('+=', '-=') and tipo not in ('int', 'float'):
                    self.error(f'{op} requiere una variable numérica', nombre)
                self.exigir(tipo, nuevo, nombre)
        elif e == 'if':
            if self.expresion(h[2]) != 'bool':
                self.error('la condición de if debe ser bool', h[0])
            self.sentencia(h[4])
            if len(h) > 5:
                self.sentencia(h[6])
        elif e == 'while':
            if self.expresion(h[2]) != 'bool':
                self.error('la condición de while debe ser bool', h[0])
            self.sentencia(h[4])
        elif e == 'do_while':
            self.sentencia(h[1])
            if self.expresion(h[4]) != 'bool':
                self.error('la condición de do-while debe ser bool', h[0])
        elif e == 'for':
            self.entrar()
            try:
                partes = h[2:-2]
                indices = [i for i, x in enumerate(partes) if x.etiqueta == ';']
                if len(indices) != 2:
                    self.error('estructura for incorrecta', h[0])
                ini = partes[:indices[0]]
                cond = partes[indices[0]+1:indices[1]]
                paso = partes[indices[1]+1:]
                if ini:
                    self.sentencia(ini[0])
                if cond and self.expresion(cond[0]) != 'bool':
                    self.error('la condición de for debe ser bool', h[0])
                if paso:
                    self.sentencia(paso[0])
                self.sentencia(h[-1])
            finally:
                self.salir()
        elif e == 'switch':
            if self.expresion(h[2]) != 'int':
                self.error('switch requiere expresión int', h[0])
            self.entrar()
            try:
                for caso in h[5:-1]:
                    for s in caso.hijos:
                        if s.etiqueta not in ('case', 'default', 'NUM', ':'):
                            self.sentencia(s)
            finally:
                self.salir()
        elif e == 'return':
            if len(h) == 2:
                if self.retorno != 'void':
                    self.error(f'return sin valor en función {self.retorno}', h[0])
            else:
                if self.retorno == 'void':
                    self.error('return con valor en función void', h[0])
                self.exigir(self.retorno, self.expresion(h[1]), h[0])
        elif e == 'salida':
            self.expresion(h[2])
        elif e == 'llamada_sent':
            self.llamada(h[0])
        elif e in ('break', 'continue'):
            pass  # Validación de contexto de bucle queda fuera del mínimo de la fase.
        else:
            self.error(f'sentencia no soportada: {e}', n)

    def analizar(self, arbol):
        # Registrar firmas antes de recorrer cuerpos; admite llamadas entre funciones.
        funciones = [n for n in arbol.hijos if n.etiqueta == 'funcion']
        for f in funciones:
            nombre = f.hijos[1]
            if nombre.valor in self.funciones:
                self.error(f"función '{nombre.valor}' redeclarada", nombre)
            params = [p for p in f.hijos[3].hijos if p.etiqueta == 'param']
            self.funciones[nombre.valor] = (self.tipo_decl(f), [self.tipo_decl(p) for p in params])
        for f in funciones:
            self.retorno = self.tipo_decl(f)
            self.entrar()
            try:
                for p in f.hijos[3].hijos:
                    if p.etiqueta == 'param':
                        self.declarar(p.hijos[1], self.tipo_decl(p))
                # El bloque exterior de función comparte ámbito con sus parámetros.
                for s in f.hijos[5].hijos[1:-1]:
                    self.sentencia(s)
            finally:
                self.salir()
        return True

def analizar_semantica(arbol):
    return AnalizadorSemantico().analizar(arbol)
