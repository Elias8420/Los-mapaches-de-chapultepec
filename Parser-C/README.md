
# Analizador de C++ — Fase 1

**Asignatura:** Teoría de Programación  
**Proyecto:** TLP02-2026  
**Lenguaje de implementación:** Python 3  
**Lenguaje analizado:** Subconjunto de C++  
**Fase:** 1 — Analizador léxico y semántico

---


## Integrantes del grupo

**Universidad:** Universidad Centroamericana José Simeón Cañas (UCA)  
**Asignatura:** Teoría de Programación  
**Proyecto:** TLP02-2026 — Fase 1

| N.º | Nombre completo del estudiante | Carnet |
|:---:|---|---|
| 1 | Kelly Estefanía Ortega López | 00186321 |
| 2 | Ronald Francisco Rivas Diaz | 00131321 |
| 3 | Henry Saul Martínez Flores | 00012622 |
| 4 | Elías Ernesto Zelaya Arias | 00146322 |
| 5 | Josemaria Miguel Muñoz Romero | 00120422 |

---


## 1. Descripción del proyecto

Este proyecto consiste en el desarrollo de un analizador para un subconjunto del lenguaje C++, implementado en Python como parte de la Fase 1 de la asignatura Teoría de Programación.

El objetivo principal es implementar un analizador léxico y un analizador semántico que permitan identificar los componentes del código fuente y verificar determinadas reglas del lenguaje.

El sistema integra tres etapas:

1. **Análisis léxico:** identifica los tokens del código fuente.
2. **Análisis sintáctico:** verifica que las instrucciones cumplan la gramática definida.
3. **Análisis semántico:** comprueba reglas relacionadas con variables, tipos de datos y ámbitos.

Aunque la Fase 1 se centra en el análisis léxico y semántico, también se incorporó un analizador sintáctico mediante descenso recursivo y la generación de árboles sintácticos como componentes de apoyo.

El programa permite identificar errores e informar su ubicación mediante números de línea y columna, cuando esta información está disponible.

---

## 2. Objetivos

### Objetivo general

Desarrollar un analizador léxico y semántico para un subconjunto de C++, utilizando Python y aplicando los fundamentos de lenguajes formales y teoría de programación.

### Objetivos específicos

- Implementar un analizador léxico que identifique palabras reservadas, identificadores, números y operadores.
- Definir formalmente los tokens del lenguaje mediante expresiones regulares.
- Desarrollar un analizador sintáctico mediante descenso recursivo.
- Construir y visualizar árboles sintácticos.
- Implementar comprobaciones semánticas de variables, tipos de datos y ámbitos.
- Detectar y reportar errores en el código fuente.
- Validar el funcionamiento mediante pruebas automatizadas.
- Relacionar el proyecto con la jerarquía de Chomsky y las limitaciones de una gramática libre de contexto.

---

## 3. Tecnologías utilizadas

- Python 3.
- C++ como lenguaje de entrada.
- Visual Studio Code.
- Git y GitHub.
- Expresiones regulares (`re`).
- `dataclasses`.
- `unittest`.
- `pathlib`.

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
    ├── .gitignore
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
         ANÁLISIS LÉXICO
             lexer.py
                |
                v
          Lista de tokens
                |
                v
       ANÁLISIS SINTÁCTICO
             parser.py
                |
                v
         Árbol sintáctico
             tree.py
                |
                v
       ANÁLISIS SEMÁNTICO
           semantico.py
                |
                v
          Resultado final
                |
         +------+------+
         |             |
         v             v
    Código válido   Error detectado
         |             |
         v             v
      Mensaje OK    Descripción
                   del problema
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

### 6.1 Estructura de un token

```python
@dataclass
class Token:
    tipo: str
    valor: str
    linea: int
    col: int
```

### 6.2 Elementos reconocidos

| Categoría | Ejemplos |
|---|---|
| Palabras reservadas | `int`, `float`, `bool`, `if`, `while` |
| Identificadores | `edad`, `numero`, `promedio` |
| Números | `10`, `25`, `3.14` |
| Operadores aritméticos | `+`, `-`, `*`, `/` |
| Operadores relacionales | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Operadores lógicos | `&&`, `\|\|`, `!` |
| Asignaciones | `=`, `+=`, `-=` |
| Incrementos | `++`, `--` |
| Delimitadores | `(`, `)`, `{`, `}`, `;`, `,` |
| Comentarios | `// comentario` |
| Directivas | `#include <iostream>` |

Los espacios y comentarios de una línea se descartan durante el análisis.

### 6.3 Ejemplo

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

## 7. Definición formal del conjunto de tokens

El conjunto de tokens del subconjunto de C++ se define mediante expresiones regulares.

En el archivo `lexer.py`, las estructuras `ESPECIFICACION` y `PALABRAS_RESERVADAS` establecen las categorías de elementos reconocidos.

### 7.1 Palabras reservadas

Las palabras reservadas consideradas incluyen:

```text
int, float, bool, void, if, else, while, do,
for, switch, case, default, break, continue,
return, cout, true, false, using, namespace
```

Estas palabras tienen un significado específico dentro del lenguaje y se diferencian de los identificadores comunes.

### 7.2 Identificadores (ID)

Los identificadores representan nombres de variables y funciones.

**Expresión regular:**

```regex
[A-Za-z_]\w*
```

Ejemplos válidos:

```text
edad
promedio
numero1
_contador
```

### 7.3 Literales numéricos (NUM)

Los literales numéricos representan números enteros y decimales.

**Expresión regular:**

```regex
\d+(?:\.\d+)?
```

Ejemplos:

```text
10
25
3.14
100.5
```

### 7.4 Directivas (INCLUDE)

Se contempla el reconocimiento de directivas de inclusión.

**Expresión regular:**

```regex
\#include[ \t]*<[A-Za-z_][\w./]*>
```

Ejemplo:

```cpp
#include <iostream>
```

### 7.5 Operadores compuestos (OP2)

Los operadores compuestos incluyen comparaciones, operadores lógicos, incrementos y asignaciones compuestas.

**Expresión regular:**

```regex
==|!=|<=|>=|&&|\|\||<<|\+\+|--|\+=|-=
```

Ejemplos:

```cpp
edad += 1;
contador++;
promedio >= 10;
```

### 7.6 Operadores simples y delimitadores

Se reconocen operadores aritméticos, relacionales, lógicos y de asignación, además de símbolos de agrupación.

**Expresión regular:**

```regex
[+\-*/<>=!(){};:,]
```

Ejemplos:

```text
+  -  *  /  <  >  =  !
(  )  {  }  ;  ,
```

### 7.7 Comentarios

Los comentarios de una línea se reconocen mediante:

```regex
//[^\n]*
```

Ejemplo:

```cpp
// Declaración de una variable
int edad = 20;
```

Los comentarios se descartan durante la generación de tokens utilizados por las siguientes etapas.

### 7.8 Espacios y saltos de línea

Los espacios y tabulaciones se reconocen mediante:

```regex
[ \t\r]+
```

Los saltos de línea permiten actualizar la posición del analizador para informar correctamente la ubicación de los tokens y errores.

### 7.9 Detección de números inválidos

El analizador contempla comprobaciones para identificar formatos numéricos incorrectos.

Entre ellos se encuentran secuencias con puntos decimales mal formados o combinaciones no válidas de números y letras.

Por ejemplo:

```cpp
int numero = 12.3.4;
```

El analizador debe identificar el formato incorrecto según las reglas implementadas.

### 7.10 Detección de caracteres no reconocidos

Cuando un carácter no corresponde a ninguno de los patrones admitidos, se genera un error léxico.

Ejemplo:

```cpp
int edad = 20 @ 5;
```

El carácter `@` no pertenece al conjunto de tokens reconocidos.

### 7.11 Relación con los lenguajes regulares

Las expresiones regulares permiten definir patrones para reconocer tokens.

En la jerarquía de Chomsky, estos patrones se relacionan con los **lenguajes regulares**, que pueden reconocerse mediante autómatas finitos.

Por esta razón, el analizador léxico constituye una aplicación práctica de los lenguajes regulares.

---

## 8. Análisis sintáctico

El analizador sintáctico está implementado mediante descenso recursivo.

Esta técnica utiliza funciones que representan las reglas de la gramática.

El analizador verifica que los tokens se encuentren organizados correctamente.

### 8.1 Estructuras del subconjunto

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

### 8.2 Árbol de análisis sintáctico

El archivo `tree.py` define la clase `Nodo`, que permite representar las estructuras reconocidas.

| Elemento | Descripción |
|---|---|
| `etiqueta` | Nombre del nodo. |
| `hijos` | Lista de nodos secundarios. |
| `valor` | Valor asociado al nodo. |
| `imprimir()` | Muestra el árbol en consola. |
| `a_nltk()` | Convierte el árbol al formato de NLTK. |

El árbol conserva elementos de la gramática, como paréntesis, llaves y puntos y coma.

---

## 9. Análisis semántico

El análisis semántico permite comprobar que las instrucciones sintácticamente válidas respeten las reglas semánticas implementadas.

El archivo encargado de esta etapa es `semantico.py`.

### 9.1 Variables no declaradas

Detecta cuando se utiliza una variable que no ha sido declarada previamente.

**Ejemplo incorrecto:**

```cpp
int main() {
    edad = 20;
    return 0;
}
```

**Resultado esperado:**

```text
ERROR: Línea 2, col 5: variable 'edad' utilizada sin declaración previa
```

### 9.2 Redeclaración de variables

Detecta cuando una variable se declara más de una vez dentro del mismo ámbito.

**Ejemplo incorrecto:**

```cpp
int main() {
    int edad = 20;
    int edad = 25;
    return 0;
}
```

**Resultado esperado:**

```text
ERROR: Línea 3, col 9: redeclaración de 'edad' en el mismo ámbito
```

### 9.3 Incompatibilidad de tipos

Comprueba que los tipos de datos sean compatibles con las operaciones y asignaciones permitidas.

**Ejemplo incorrecto:**

```cpp
int main() {
    int edad = true;
    return 0;
}
```

**Resultado esperado:**

```text
ERROR: Línea 2, col 9: tipos incompatibles: se esperaba int, se obtuvo bool
```

### 9.4 Control de ámbitos

Las variables declaradas dentro de un bloque solamente pueden utilizarse en los ámbitos donde son visibles.

**Ejemplo incorrecto:**

```cpp
int main() {
    if (true) {
        int numero = 10;
    }

    numero = 20;
    return 0;
}
```

**Resultado esperado:**

```text
ERROR: Línea 5, col 5: variable 'numero' utilizada sin declaración previa
```

Esto permite comprobar el manejo de ámbitos mediante una tabla de símbolos.

### 9.5 Tabla de símbolos

La tabla de símbolos permite almacenar información sobre las variables declaradas.

Entre los datos utilizados se encuentran:

- Nombre del identificador.
- Tipo de dato.
- Ámbito de declaración.

Esta información permite realizar comprobaciones que dependen de declaraciones anteriores y del contexto del programa.

---

## 10. Ejemplo de código válido

El archivo `ejemplo.cpp` contiene un programa que permite comprobar el funcionamiento de los analizadores.

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

```text
OK: análisis léxico, sintáctico y semántico completados
```

Esto indica que el código cumple las reglas implementadas para el subconjunto de C++.

---

## 11. Instrucciones de ejecución

### 11.1 Requisitos

Es necesario tener instalado Python 3.

Para comprobarlo:

```bash
python --version
```

### 11.2 Acceder al proyecto

Desde la carpeta principal del repositorio:

```bash
cd Parser-C
```

Si ya se encuentra dentro de `Parser-C`, no es necesario ejecutar este comando.

### 11.3 Ejecutar el ejemplo válido

```bash
python ejecutar.py ejemplo.cpp
```

**Resultado esperado:**

```text
OK: análisis léxico, sintáctico y semántico completados
```

### 11.4 Mostrar los tokens

```bash
python ejecutar.py ejemplo.cpp --tokens
```

Esta opción muestra la lista de tokens identificados.

### 11.5 Mostrar el árbol sintáctico

```bash
python ejecutar.py ejemplo.cpp --arbol
```

Esta opción muestra la estructura del árbol en la terminal.

### 11.6 Mostrar tokens y árbol

```bash
python ejecutar.py ejemplo.cpp --tokens --arbol
```

Esta instrucción permite observar el resultado de las diferentes etapas del análisis.

---

## 12. Pruebas automatizadas

Para verificar el funcionamiento del sistema se implementaron pruebas utilizando la biblioteca `unittest` de Python.

Las pruebas se encuentran en:

```text
Parser-C/pruebas/test_fase1.py
```

### 12.1 Casos de prueba

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

### 12.2 Ejecutar las pruebas

Desde la carpeta `Parser-C`:

```bash
python -m unittest discover -s pruebas -v
```

### 12.3 Resultado obtenido

Durante la ejecución de las pruebas se obtuvo:

```text
Ran 13 tests in 0.003s

OK
```

Las 13 pruebas finalizaron correctamente.

Este resultado demuestra que los casos automatizados implementados se ejecutaron sin fallos en la versión evaluada.

---

## 13. Manejo de errores

El analizador diferencia errores según la etapa en la que se detectan.

### 13.1 Errores léxicos

Se producen cuando el código contiene caracteres no reconocidos.

**Ejemplo:**

```cpp
int main() {
    int edad = 20;
    edad = 20 @ 5;
    return 0;
}
```

El analizador identifica el carácter `@` como inválido.

### 13.2 Errores sintácticos

Se producen cuando las instrucciones no cumplen las reglas gramaticales.

**Ejemplo:**

```cpp
int main() {
    int edad = 20
    return 0;
}
```

En este caso falta el punto y coma después de la declaración.

### 13.3 Errores semánticos

Se producen cuando el código tiene una estructura sintáctica válida, pero incumple alguna regla semántica.

**Ejemplo:**

```cpp
int main() {
    int edad = 20;
    int edad = 25;
    return 0;
}
```

En este caso se detecta una redeclaración de variable dentro del mismo ámbito.

---

## 14. Reflexión teórica: jerarquía de Chomsky y límites de una CFG

La jerarquía de Chomsky clasifica los lenguajes formales según su complejidad y los mecanismos necesarios para reconocerlos.

Esta clasificación permite relacionar los analizadores desarrollados con los fundamentos teóricos de la asignatura.

### 14.1 Análisis léxico y lenguajes regulares

El análisis léxico se relaciona con los **lenguajes regulares**, correspondientes al tipo 3 de la jerarquía de Chomsky.

Estos lenguajes pueden describirse mediante expresiones regulares y reconocerse mediante autómatas finitos.

En nuestro proyecto, las expresiones regulares permiten identificar:

- Palabras reservadas.
- Identificadores.
- Literales numéricos.
- Operadores.
- Delimitadores.

Por ejemplo, la expresión regular:

```regex
[A-Za-z_]\w*
```

permite reconocer identificadores.

Esto demuestra la aplicación práctica de los lenguajes regulares en el procesamiento del código fuente.

### 14.2 Análisis sintáctico y lenguajes libres de contexto

El análisis sintáctico se relaciona con los **lenguajes libres de contexto**, correspondientes al tipo 2 de la jerarquía de Chomsky.

Las gramáticas libres de contexto, conocidas como CFG (*Context-Free Grammars*), permiten describir estructuras anidadas como:

- Bloques de instrucciones.
- Expresiones aritméticas.
- Funciones.
- Condicionales.
- Ciclos.
- Paréntesis y llaves.

En nuestro proyecto, el analizador sintáctico utiliza descenso recursivo para reconocer las estructuras definidas por la gramática.

### 14.3 Limitaciones de una gramática libre de contexto

Aunque una CFG permite representar estructuras sintácticas, no puede verificar por sí sola todas las reglas semánticas de un lenguaje de programación.

Existen reglas que dependen del contexto y de relaciones entre diferentes partes del programa.

#### Declaración previa de variables

Para comprobar que una variable fue declarada antes de utilizarse, es necesario conservar información sobre las declaraciones anteriores.

Ejemplo:

```cpp
int main() {
    edad = 20;
    return 0;
}
```

La instrucción puede tener una estructura sintáctica correcta, pero presenta un error semántico porque `edad` no fue declarada previamente.

Esta comprobación requiere consultar una tabla de símbolos.

#### Control de ámbitos

Las variables declaradas dentro de un bloque solamente deben ser accesibles en los ámbitos donde son visibles.

Por ejemplo:

```cpp
int main() {
    if (true) {
        int numero = 10;
    }

    numero = 20;
    return 0;
}
```

La variable `numero` fue declarada dentro de un bloque y no puede utilizarse fuera de él.

Para identificar este problema es necesario conservar información sobre los ámbitos activos.

#### Redeclaración de variables

Impedir dos declaraciones de una misma variable dentro del mismo ámbito requiere consultar las declaraciones registradas previamente.

Ejemplo:

```cpp
int main() {
    int edad = 20;
    int edad = 25;
    return 0;
}
```

El analizador semántico identifica que `edad` ya fue declarada dentro del mismo ámbito.

#### Compatibilidad de tipos

Comprobar si una asignación u operación es válida requiere conocer los tipos de datos involucrados.

Ejemplo:

```cpp
int main() {
    int edad = true;
    return 0;
}
```

La estructura de la instrucción es reconocible, pero la asignación incumple las reglas de compatibilidad de tipos implementadas.

### 14.4 Importancia del analizador semántico

Estas comprobaciones requieren información adicional a la estructura gramatical.

Por esta razón, nuestro proyecto incorpora un analizador semántico que utiliza una tabla de símbolos para registrar identificadores, tipos de datos y ámbitos.

De esta manera, el sistema puede identificar errores que no pueden detectarse únicamente mediante el análisis sintáctico.

### 14.5 Relación con la Fase 2

La separación entre análisis léxico, sintáctico y semántico permite organizar el procesamiento del código fuente.

Esta estructura proporciona una base para reutilizar y ampliar los componentes desarrollados durante la Fase 2 del proyecto.

---

## 15. Limitaciones del analizador

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

## 16. Resultados del proyecto

Durante el desarrollo de la Fase 1 se implementaron los componentes necesarios para procesar código fuente perteneciente al subconjunto definido.

Se obtuvieron los siguientes resultados:

- Identificación de tokens mediante expresiones regulares.
- Definición formal de las categorías de tokens.
- Registro de línea y columna de los tokens.
- Detección de errores léxicos.
- Análisis sintáctico mediante descenso recursivo.
- Generación de árboles sintácticos.
- Detección de variables utilizadas sin declaración previa.
- Detección de redeclaraciones.
- Comprobación de compatibilidad de tipos.
- Manejo de ámbitos de variables.
- Identificación de errores con mensajes descriptivos.
- Ejecución satisfactoria de 13 pruebas automatizadas.
- Reflexión teórica sobre la jerarquía de Chomsky y las limitaciones de una CFG.

Los resultados permiten comprobar el funcionamiento de los componentes evaluados mediante los casos de prueba desarrollados.

---

## 17. Conclusiones

El desarrollo del analizador permitió aplicar conceptos fundamentales de teoría de programación, incluyendo lenguajes regulares, expresiones regulares, gramáticas formales, análisis sintáctico y comprobaciones semánticas.

La implementación del analizador léxico permitió reconocer los diferentes componentes del código fuente mediante expresiones regulares, relacionando su funcionamiento con los lenguajes regulares de la jerarquía de Chomsky.

El analizador sintáctico, implementado mediante descenso recursivo, facilitó la organización de las reglas gramaticales y la construcción de árboles de análisis.

La incorporación del análisis semántico permitió detectar errores que no pueden identificarse únicamente mediante el análisis sintáctico, como variables no declaradas, redeclaraciones e incompatibilidades de tipos.

Asimismo, las pruebas automatizadas permitieron validar diferentes escenarios de funcionamiento, tanto con programas válidos como con programas que contienen errores.

Finalmente, la separación de responsabilidades entre los diferentes analizadores proporciona una base organizada para futuras ampliaciones del proyecto.

---

## 18. Estado del proyecto

**Fase:** 1

**Lenguaje de implementación:** Python 3

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

**Enfoque de la entrega:** Analizador léxico, analizador semántico y video de demostración.

**Repositorio:** https://github.com/Elias8420/teo_fase_1
