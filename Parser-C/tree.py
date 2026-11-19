class Nodo:
    def __init__(self, etiqueta, hijos=None, valor=None, linea=None, col=None):
        self.etiqueta = etiqueta
        self.hijos = hijos if hijos is not None else []
        self.valor = valor
        self.linea = linea
        self.col = col  
 
    def _texto(self):
        return f"{self.etiqueta}: {self.valor}" if self.valor is not None else self.etiqueta
 
    def imprimir(self, prefijo="", ultimo=True, raiz=True):
        if raiz:
            print(self._texto())
            nuevo = ""
        else:
            print(prefijo + ("└── " if ultimo else "├── ") + self._texto())
            nuevo = prefijo + ("    " if ultimo else "│   ")
        for i, hijo in enumerate(self.hijos):
            hijo.imprimir(nuevo, i == len(self.hijos) - 1, raiz=False)
 
    def a_nltk(self):
        """Convierte a nltk.Tree (útil para la Fase 2 y para dibujar)."""
        from nltk import Tree
        if not self.hijos:
            return Tree(self.etiqueta, [str(self.valor)] if self.valor is not None else [])
        return Tree(self.etiqueta, [h.a_nltk() for h in self.hijos])
