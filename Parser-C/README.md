
# Analizador de C++ — Fase 1

## 1. Descripción del proyecto

Este proyecto consiste en el desarrollo de un analizador para un subconjunto del lenguaje C++, implementado en Python como parte de la Fase 1 de Teoría de Programación.

El sistema realiza tres tipos de análisis:

1. **Análisis léxico:** identifica los tokens del código fuente.
2. **Análisis sintáctico:** verifica que las instrucciones cumplan con la gramática definida.
3. **Análisis semántico:** comprueba reglas relacionadas con variables, tipos de datos y ámbitos.

El analizador sintáctico utiliza la técnica de descenso recursivo y genera un árbol de análisis sintáctico.

El programa también identifica errores e informa su ubicación mediante el número de línea y columna, cuando esta información está disponible.

---

## 2. Objetivos

### Objetivo general

Desarrollar un analizador para un subconjunto de C++ utilizando Python, capaz de realizar análisis léxico, sintáctico y semántico.

### Objetivos específicos

- Implementar un analizador léxico que identifique palabras reservadas, identificadores, números y operadores.
- Desarrollar un analizador sintáctico mediante descenso recursivo.
- Construir y visualizar árboles de análisis sintáctico.
- Implementar comprobaciones semánticas de variables, tipos de datos y ámbitos.
- Detectar y reportar errores en el código fuente.
- Validar el funcionamiento mediante pruebas automatizadas.

---

## 3. Tecnologías utilizadas

- Python 3
- C++ como lenguaje de entrada
- Visual Studio Code
- Expresiones regulares (`re`)
- `dataclasses`
- `unittest`
- `pathlib`

La implementación principal utiliza bibliotecas estándar de Python.

La conversión opcional de árboles a `nltk.Tree` requiere instalar NLTK.

---

## 4. Estructura del proyecto

```text
teo_fase_1/
│
├── Gramatica_es/
│   ├── gramaticas_es.py
│   ├── lexico.py
│   ├── parser_es.py
│   ├── prueba-es.py
│   ├── tree.py
│   └── README.md
│
└── Parser-C/
    ├── lexer.py
    ├── parser.py
    ├── semantico.py
    ├── tree.py
    ├── ejecutar.py
    ├── ejemplo.cpp
    ├── README.md
    │
    └── pruebas/
        └── test_fase1.py
```

### Descripción de los archivos principales

| Archivo | Función |
|---|---|
| `lexer.py` | Realiza el análisis léxico. |
| `parser.py` | Realiza el análisis sintáctico. |
| `semantico.py` | Comprueba las reglas semánticas implementadas. |
| `tree.py` | Define la estructura del árbol sintáctico. |
| `ejecutar.py` | Permite ejecutar los analizadores desde la terminal. |
| `ejemplo.cpp` | Contiene un programa de prueba válido. |
| `test_fase1.py` | Contiene las pruebas automatizadas. |
| `README.md` | Documenta el funcionamiento del proyecto. |

---

## 5. Funcionamiento general

El analizador procesa el código fuente mediante las siguientes etapas:

```text
        Código fuente C++
                |
                v
       ANALIZADOR LÉXICO
             lexer.py
                |
                v
          Lista de tokens
                |
                v
      ANALIZADOR SINTÁCTICO
             parser.py
                |
                v
       Árbol de análisis
             tree.py
                |
                v
      ANALIZADOR SEMÁNTICO
           semantico.py
                |
                v
          Resultado final
                |
        +-------+-------+
        |               |
        v               v
   Código válido    Error detectado
        |               |
        v               v
     Mensaje       Línea, columna
      de OK         y descripción
```

Si se encuentra un error, el análisis se detiene y se muestra el mensaje correspondiente.

---

## 6. Análisis léxico

El analizador léxico transforma el código fuente en una secuencia de tokens.

Cada token contiene:

- Tipo de token.
- Valor encontrado.
- Número de línea.
- Número de columna.

### Estructura de un token

```python
@dataclass
class Token:
    tipo: str
    valor: str
    linea: int
    col: int
```

### Elementos reconocidos

| Categoría | Ejemplos |
|---|---|
| Palabras reservadas | `int`, `float`, `bool`, `if`, `while` |
| Identificadores | `edad`, `numero`, `promedio` |
| Números | `10`, `25`, `3.14` |
| Operadores aritméticos | `+`, `-`, `*`, `/` |
| Operadores relacionales | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Operadores lógicos | `&&`, `||`, `!` |
| Asignaciones | `=`, `+=`, `-=` |
| Incrementos | `++`, `--` |
| Delimitadores | `(`, `)`, `{`, `}`, `;`, `,` |
| Comentarios | `// comentario` |
| Directivas | `#include <iostream>` |

Los espacios y comentarios de una línea se descartan durante el análisis.

### Ejemplo

Código fuente:

```cpp
int edad = 20;
```

Tokens generados:

```text
Token(tipo='int', valor='int', linea=1, col=1)
Token(tipo='ID', valor='edad', linea=1, col=5)
Token(tipo='=', valor='=', linea=1, col=10)
Token(tipo='NUM', valor='20', linea=1, col=12)
Token(tipo=';', valor=';', linea=1, col=14)
```

---

## 7. Análisis sintáctico

El analizador sintáctico está implementado mediante descenso recursivo.

Esta técnica utiliza funciones que representan las reglas de la gramática.

El analizador verifica que los tokens se encuentren organizados correctamente.

### Estructuras del subconjunto

El proyecto contempla estructuras como:

- Declaración de variables.
- Asignaciones.
- Expresiones aritméticas.
- Expresiones relacionales y lógicas.
- Funciones.
- Condicionales `if` y `else`.
- Ciclos `while`, `do while` y `for`.
- Estructuras `switch`, `case` y `default`.
- Instrucciones `return`, `break` y `continue`.

Estas características corresponden al subconjunto definido por la gramática del proyecto, no a la totalidad del lenguaje C++.

### Árbol de análisis sintáctico

El archivo `tree.py` define la clase `Nodo`, que permite representar las estructuras reconocidas.

Sus principales componentes son:

| Elemento | Descripción |
|---|---|
| `etiqueta` | Nombre del nodo. |
| `hijos` | Lista de nodos secundarios. |
| `valor` | Valor asociado al nodo. |
| `imprimir()` | Muestra el árbol en consola. |
| `a_nltk()` | Convierte el árbol al formato de NLTK. |

El árbol conserva elementos de la gramática, como paréntesis, llaves y puntos y coma.

---

## 8. Análisis semántico

El análisis semántico permite comprobar que las instrucciones sintácticamente válidas respeten las reglas semánticas implementadas.

El archivo encargado de esta etapa es:

```text
semantico.py
```

### Comprobaciones implementadas

#### 8.1 Variables no declaradas

Detecta cuando se utiliza una variable que no ha sido declarada previamente.

Ejemplo incorrecto:

```cpp
int main() {
    edad = 20;
    return 0;
}
```

Resultado:

```text
ERROR: Línea 2, col 5: variable 'edad' utilizada sin declaración previa
```

#### 8.2 Redeclaración de variables

Detecta cuando una variable se declara más de una vez dentro del mismo ámbito.

Ejemplo incorrecto:

```cpp
int main() {
    int edad = 20;
    int edad = 25;
    return 0;
}
```

Resultado:

```text
ERROR: Línea 3, col 9: redeclaración de 'edad' en el mismo ámbito
```

#### 8.3 Incompatibilidad de tipos

Comprueba que los tipos de datos sean compatibles con las operaciones y asignaciones permitidas.

Ejemplo incorrecto:

```cpp
int main() {
    int edad = true;
    return 0;
}
```

Resultado:

```text
ERROR: Línea 2, col 9: tipos incompatibles: se esperaba int, se obtuvo bool
```

#### 8.4 Control de ámbitos

Las variables declaradas dentro de un bloque solamente pueden utilizarse en los ámbitos donde son visibles.

Ejemplo incorrecto:

```cpp
int main() {
    if (true) {
        int numero = 10;
    }

    numero = 20;
    return 0;
}
```

Resultado:

```text
ERROR: Línea 5, col 5: variable 'numero' utilizada sin declaración previa
```

Esto permite comprobar el manejo de ámbitos mediante una tabla de símbolos.

---

## 9. Ejemplo de código válido

El archivo `ejemplo.cpp` contiene un programa que permite comprobar el funcionamiento de los tres analizadores.

### Código fuente

```cpp
int main() {
    int edad = 20;
    float promedio = edad + 2.5;
    bool aprobado = promedio >= 10;

    if (aprobado) {
        edad += 1;
    }

    return edad;
}
```

### Características evaluadas

Este programa permite comprobar:

1. Reconocimiento de palabras reservadas.
2. Identificación de variables y números.
3. Declaración de variables de distintos tipos.
4. Operaciones aritméticas.
5. Comparaciones relacionales.
6. Evaluación de condiciones booleanas.
7. Asignaciones compuestas.
8. Uso de variables declaradas previamente.
9. Construcción del árbol sintáctico.
10. Comprobación semántica del programa.

### Resultado esperado

Al ejecutar el analizador sobre este código se obtiene:

```text
OK: análisis léxico, sintáctico y semántico completados
```

Esto indica que el código cumple las reglas implementadas para el subconjunto de C++.

---

## 10. Instrucciones de ejecución

### 10.1 Requisitos

Es necesario tener instalado Python 3.

Para comprobarlo:

```powershell
python --version
```

### 10.2 Acceder al proyecto

Desde la carpeta principal del repositorio:

```powershell
cd teo_fase_1/Parser-C
```

Si ya se encuentra dentro de `Parser-C`, no es necesario ejecutar este comando.

### 10.3 Ejecutar el ejemplo válido

```powershell
python ejecutar.py ejemplo.cpp
```

Resultado esperado:

```text
OK: análisis léxico, sintáctico y semántico completados
```

### 10.4 Mostrar los tokens

```powershell
python ejecutar.py ejemplo.cpp --tokens
```

Esta opción muestra la lista de tokens identificados.

### 10.5 Mostrar el árbol sintáctico

```powershell
python ejecutar.py ejemplo.cpp --arbol
```

Esta opción muestra la estructura del árbol en la terminal.

### 10.6 Mostrar tokens y árbol

```powershell
python ejecutar.py ejemplo.cpp --tokens --arbol
```

Esta instrucción permite observar el resultado de las diferentes etapas del análisis.

---

## 11. Pruebas automatizadas

Para verificar el funcionamiento del sistema se implementaron pruebas utilizando la biblioteca `unittest` de Python.

Las pruebas se encuentran en:

```text
Parser-C/pruebas/test_fase1.py
```

### Casos de prueba

| Prueba | Descripción |
|---|---|
| `test_valido` | Comprueba un programa válido. |
| `test_tokens_posicion` | Verifica línea y columna de los tokens. |
| `test_error_caracter` | Comprueba errores léxicos. |
| `test_error_numero` | Comprueba un caso de error relacionado con números. |
| `test_error_funcion` | Comprueba un error en funciones. |
| `test_funcion` | Comprueba el análisis de funciones. |
| `test_while_do` | Comprueba estructuras repetitivas. |
| `test_for` | Comprueba el ciclo `for`. |
| `test_ambito` | Comprueba el manejo de ámbitos. |
| `test_no_declarada` | Detecta variables no declaradas. |
| `test_redeclaracion` | Detecta redeclaraciones. |
| `test_tipo` | Detecta incompatibilidad de tipos. |
| `test_sombreado` | Comprueba el sombreado de variables. |

### Ejecutar las pruebas

Desde la carpeta `Parser-C`:

```powershell
python -m unittest discover -s pruebas -v
```

### Resultado obtenido

Durante la ejecución de las pruebas se obtuvo:

```text
Ran 13 tests in 0.003s

OK
```

Las 13 pruebas finalizaron correctamente.

Este resultado demuestra que los casos automatizados implementados se ejecutaron sin fallos en la versión evaluada.

---

## 12. Manejo de errores

El analizador diferencia errores según la etapa en la que se detectan.

### Errores léxicos

Se producen cuando el código contiene caracteres no reconocidos.

Ejemplo:

```cpp
int main() {
    int edad = 20;
    edad = 20 @ 5;
    return 0;
}
```

El analizador identifica el carácter `@` como inválido.

### Errores sintácticos

Se producen cuando las instrucciones no cumplen las reglas gramaticales.

Ejemplo:

```cpp
int main() {
    int edad = 20
    return 0;
}
```

En este caso falta el punto y coma después de la declaración.

### Errores semánticos

Se producen cuando el código tiene una estructura sintáctica válida, pero incumple alguna regla semántica.

Ejemplo:

```cpp
int main() {
    int edad = 20;
    int edad = 25;
    return 0;
}
```

En este caso se detecta una redeclaración de variable dentro del mismo ámbito.

---

## 13. Limitaciones del analizador

El proyecto implementa un subconjunto de C++, por lo que no pretende reconocer todas las características del lenguaje.

Entre las limitaciones se encuentran:

- No admite cadenas de texto.
- No implementa arreglos.
- No implementa punteros.
- No implementa clases.
- No admite declaraciones globales.
- `cout` está limitado a una expresión según la gramática definida.
- `case` acepta únicamente números.
- No permite encadenar comparaciones como `a < b < c`.
- Las comparaciones relacionales y de igualdad comparten nivel de precedencia en la gramática implementada.
- La inicialización y el paso del `for` se encuentran restringidos a las formas admitidas por el parser.

Estas limitaciones corresponden al alcance definido para el proyecto académico.

---

## 14. Resultados del proyecto

Durante el desarrollo de la Fase 1 se implementaron los componentes necesarios para procesar código fuente perteneciente al subconjunto definido.

Se obtuvieron los siguientes resultados:

- Identificación de tokens mediante expresiones regulares.
- Análisis sintáctico mediante descenso recursivo.
- Generación de árboles de análisis sintáctico.
- Detección de variables utilizadas sin declaración previa.
- Detección de redeclaraciones.
- Comprobación de compatibilidad de tipos.
- Manejo de ámbitos de variables.
- Identificación de errores con mensajes descriptivos.
- Ejecución de 13 pruebas automatizadas exitosas.

Los resultados permiten comprobar el funcionamiento de los componentes evaluados mediante los casos de prueba desarrollados.

---

## 15. Conclusiones

El desarrollo del analizador permitió aplicar conceptos fundamentales de teoría de programación, incluyendo análisis léxico, gramáticas formales, análisis sintáctico y comprobaciones semánticas.

La implementación mediante descenso recursivo facilitó la organización de las reglas gramaticales en funciones y la construcción de árboles de análisis.

La incorporación del análisis semántico permitió detectar errores que no pueden identificarse únicamente mediante el análisis sintáctico, como variables no declaradas, redeclaraciones e incompatibilidades de tipos.

Finalmente, las pruebas automatizadas permitieron validar diferentes escenarios de funcionamiento, tanto con programas válidos como con programas que contienen errores.

El proyecto constituye una base para futuras ampliaciones del subconjunto de C++ y de las funcionalidades del analizador.

---

## 16. Estado del proyecto

**Fase:** 1

**Lenguaje de implementación:** Python

**Lenguaje analizado:** Subconjunto de C++

**Técnica de análisis sintáctico:** Descenso recursivo

**Componentes desarrollados:**

- Analizador léxico.
- Analizador sintáctico.
- Analizador semántico.
- Generador de árboles.
- Ejecutor desde terminal.
- Pruebas automatizadas.

**Pruebas automatizadas ejecutadas:** 13

**Resultado de las pruebas:** OK
