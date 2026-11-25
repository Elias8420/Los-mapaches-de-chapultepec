# Proyecto TLP02-2026 — Teoría de Programación

## Fase 2: Gramáticas formales y lenguaje natural: experimentando los límites de la jerarquía de Chomsky

**Universidad Centroamericana José Simeón Cañas (UCA)**

**Ciclo 02-2026**

---

## 1. Integrantes del equipo

| N.º | Nombre completo | Carnet |
|---|---|---|
| 1 | Kelly Estefanía Ortega López | 00186321 |
| 2 | Ronald Francisco Rivas Diaz | 00131321 |
| 3 | Henry Saul Martínez Flores | 00012622 |
| 4 | Elías Ernesto Zelaya Arias | 00146322 |
| 5 | Josemaria Miguel Muñoz Romero | 00120422 |

---

## 2. Descripción del proyecto

La segunda fase del proyecto consiste en el desarrollo de un analizador para un subconjunto del lenguaje español mediante gramáticas libres de contexto (CFG).

Se implementaron cuatro versiones incrementales de una gramática, incorporando progresivamente estructuras sintácticas, concordancia gramatical, subordinación, recursividad y modificadores.

Además, se incorporó un analizador semántico y se realizó una comparación experimental con herramientas modernas de procesamiento del lenguaje natural (NLP), como spaCy y Hugging Face, y modelos de lenguaje de gran tamaño (LLM).

El propósito es identificar las capacidades y limitaciones de las gramáticas libres de contexto en el procesamiento del lenguaje natural, relacionando los resultados obtenidos con la jerarquía de Chomsky.

---

## 3. Objetivos

### Objetivo general

Analizar las capacidades y limitaciones de las gramáticas libres de contexto aplicadas al lenguaje natural mediante la implementación de un analizador del español y su comparación con herramientas modernas de NLP y modelos LLM.

### Objetivos específicos

- Diseñar cuatro versiones incrementales de una gramática libre de contexto.
- Implementar un analizador sintáctico descendente recursivo.
- Generar árboles sintácticos en consola y mediante una interfaz gráfica.
- Analizar fenómenos de concordancia, ambigüedad y recursividad.
- Evaluar las gramáticas mediante un conjunto de 60 oraciones.
- Comparar los resultados con spaCy, Hugging Face y modelos LLM.
- Identificar las limitaciones de las CFG mediante resultados experimentales.

---

## 4. Tecnologías utilizadas

- Python 3.
- NLTK.
- Tkinter.
- spaCy.
- Hugging Face Transformers.
- PyTorch.
- Modelos LLM mediante API.
- JSON.
- CSV.
- Git y GitHub.

---

## 5. Estructura del proyecto

```text
Gramatica_es/
│
├── gramaticas_es.py
├── lexico.py
├── parser_es.py
├── semantico.py
├── tree.py
├── prueba-es.py
├── eval_cfg.py
├── benchmark_nlp.py
├── llm_experiment.py
├── metrics.py
├── README.md
│
├── data/
│   └── test_set_60.json
│
├── results/
├── results_spacy/
├── results_batch/
├── results_batch_2/
├── results_batch_3/
├── results_batch_4/
├── results_batch_few/
├── results_batch_few_2/
├── results_batch_few_3/
└── results_batch_few_4/
```

### Descripción de los archivos

| Archivo | Descripción |
|---|---|
| `gramaticas_es.py` | Contiene las cuatro versiones de las gramáticas del español. |
| `lexico.py` | Define el vocabulario y las categorías léxicas. |
| `parser_es.py` | Implementa el analizador sintáctico y genera los árboles. |
| `semantico.py` | Realiza verificaciones adicionales de compatibilidad de rasgos. |
| `tree.py` | Representa los nodos y permite convertir los árboles al formato NLTK. |
| `prueba-es.py` | Ejecuta pruebas individuales y reportes de las gramáticas. |
| `eval_cfg.py` | Evalúa las gramáticas sobre las 60 oraciones. |
| `benchmark_nlp.py` | Realiza experimentos con spaCy y Hugging Face. |
| `llm_experiment.py` | Ejecuta experimentos con modelos LLM mediante API. |
| `metrics.py` | Calcula las métricas de evaluación. |
| `test_set_60.json` | Contiene las 60 oraciones del conjunto experimental. |
| `results*/` | Almacena métricas, predicciones y registros experimentales. |

---

## 6. Versiones de la gramática

Se desarrollaron cuatro versiones incrementales de una gramática libre de contexto.

| Versión | Cantidad de reglas | Características |
|---|---:|---|
| CFG v1 | 9 | Estructuras básicas de sujeto, verbo y objeto. |
| CFG v2 | 43 | Concordancia de género, número y persona. |
| CFG v3 | 73 | Oraciones subordinadas, recursividad y modos verbales. |
| CFG v4 | 103 | Adjetivos, adverbios y frases preposicionales. |
| CFG v4 + Semántico | 103 | Gramática v4 con verificaciones adicionales de rasgos. |

### CFG v1

Representa estructuras básicas del español mediante reglas de sujeto, verbo y objeto.

### CFG v2

Incorpora restricciones de concordancia gramatical para controlar la compatibilidad de género, número y persona.

### CFG v3

Agrega estructuras subordinadas y recursivas, además del tratamiento de los modos indicativo y subjuntivo.

### CFG v4

Amplía la cobertura mediante modificadores adjetivales, adverbiales y frases preposicionales.

### CFG v4 + Semántico

Incorpora verificaciones adicionales sobre los árboles generados por la cuarta versión de la gramática.

---

## 7. Instalación y configuración

### 7.1. Requisitos

- Python 3 instalado.
- Git.
- Terminal de comandos.
- Conexión a Internet para instalar dependencias y descargar modelos externos.
- Entorno gráfico para visualizar los árboles mediante NLTK.

### 7.2. Acceder a la carpeta del proyecto

Desde la raíz del repositorio:

```bash
cd Gramatica_es
```

### 7.3. Instalar NLTK

```bash
python -m pip install nltk
```

### 7.4. Verificar Tkinter

```bash
python -m tkinter
```

Si Tkinter está disponible, se abrirá una ventana gráfica de prueba.

### 7.5. Instalar dependencias de NLP

```bash
python -m pip install spacy transformers torch
```

Descargar el modelo del español utilizado por spaCy:

```bash
python -m spacy download es_core_news_md
```

### 7.6. Instalar dependencias para modelos LLM

```bash
python -m pip install google-genai openai
```

Las dependencias externas son necesarias para reproducir los experimentos NLP y LLM, pero no para ejecutar las gramáticas en consola.

---

## 8. Ejecución del analizador sintáctico

### 8.1. Ejecutar CFG v1

```bash
python prueba-es.py v1 "el gato come el pescado"
```

### 8.2. Ejecutar CFG v2

```bash
python prueba-es.py v2 "el gato come el pescado"
```

### 8.3. Ejecutar CFG v3

```bash
python prueba-es.py v3 "maría dice que juan cree que el niño duerme"
```

### 8.4. Ejecutar CFG v4

```bash
python prueba-es.py v4 "el niño vio la casa con el telescopio"
```

### 8.5. Mostrar el reporte general de las gramáticas

```bash
python prueba-es.py
```

### 8.6. Consultar las reglas de una gramática

```bash
python prueba-es.py gramatica v4
```

---

## 9. Generación de árboles sintácticos

El analizador permite representar la estructura de las oraciones mediante árboles sintácticos.

Los árboles pueden visualizarse de dos formas:

- Representación jerárquica en consola.
- Representación gráfica mediante NLTK y Tkinter.

### 9.1. Visualización en consola

```bash
python prueba-es.py v4 "el gato come el pescado"
```

Resultado:

```text
Aceptada por la versión 4: 1 árbol(es)

O
├── SNs_3s
│   └── SN_ms
│       ├── Det_ms: el
│       └── N_ms: gato
└── SV_3s
    └── SVn_3s
        ├── Vt_3s: come
        └── SNo
            └── SN_ms
                ├── Det_ms: el
                └── N_ms: pescado
```

### 9.2. Visualización gráfica

Se incorporó el argumento opcional `--grafico` para visualizar los árboles sintácticos mediante una ventana gráfica.

```bash
python prueba-es.py v4 "el gato come el pescado" --grafico
```

La implementación utiliza el método `a_nltk()` de la clase Nodo, definido en `tree.py`.

```python
a.a_nltk().draw()
```

La opción gráfica no modifica las reglas gramaticales ni los resultados del análisis sintáctico.

---

## 10. Casos de prueba

### 10.1. Oración válida

```bash
python prueba-es.py v4 "el gato come el pescado"
```

Resultado esperado: oración aceptada y generación de un árbol sintáctico.

### 10.2. Error de concordancia

```bash
python prueba-es.py v1 "la gato come el pescado"
```

```bash
python prueba-es.py v2 "la gato come el pescado"
```

La primera versión puede aceptar la oración debido a la ausencia de restricciones de concordancia.

La segunda versión incorpora restricciones de género y permite detectar la incompatibilidad entre el determinante y el sustantivo.

### 10.3. Recursividad

```bash
python prueba-es.py v3 "maría dice que juan cree que el niño duerme"
```

Este ejemplo permite representar oraciones subordinadas dentro de otras oraciones, demostrando la capacidad recursiva de la gramática.

### 10.4. Tiempos verbales

Presente:

```bash
python prueba-es.py v4 "el gato come el pescado"
```

Pretérito:

```bash
python prueba-es.py v4 "el gato comió el pescado"
```

Ambas oraciones fueron aceptadas por la cuarta versión de la gramática.

### 10.5. Ambigüedad sintáctica

```bash
python prueba-es.py v4 "el niño vio la casa con el telescopio" --grafico
```

Esta oración presenta dos interpretaciones sintácticas:

1. El niño utiliza el telescopio para observar la casa.
2. La casa es la que tiene el telescopio.

En la primera interpretación, la frase preposicional modifica al verbo.

En la segunda interpretación, la frase preposicional modifica al sustantivo.

El analizador genera dos árboles sintácticos diferentes para una misma oración.

Al cerrar la primera ventana gráfica, se muestra el siguiente árbol.

---

## 11. Conjunto experimental

El conjunto de pruebas se encuentra en:

```text
data/test_set_60.json
```

Está compuesto por 60 oraciones clasificadas según tres niveles de complejidad.

| Nivel | Cantidad de oraciones |
|---|---:|
| Simple | 20 |
| Intermedio | 20 |
| Complejo | 20 |
| Total | 60 |

### Distribución según validez

| Clasificación | Cantidad |
|---|---:|
| Oraciones válidas | 50 |
| Oraciones inválidas | 10 |
| Total | 60 |

El conjunto permite evaluar la capacidad de los diferentes sistemas para aceptar oraciones válidas y rechazar oraciones inválidas.

---

## 12. Evaluación de las gramáticas CFG

Para ejecutar la evaluación experimental:

```bash
python eval_cfg.py
```

Para reproducir los resultados sin sobrescribir las evidencias originales:

```bash
python eval_cfg.py --out-dir reproduccion_cfg
```

Se generan los siguientes archivos:

```text
reproduccion_cfg/
├── metrics_cfg_60.csv
└── cfg_detalles.json
```

Estos archivos contienen las métricas globales, las métricas por nivel de complejidad y los detalles de las evaluaciones individuales.

---

## 13. Comparación con herramientas modernas de NLP

### 13.1. spaCy

Se utiliza spaCy como herramienta de procesamiento del lenguaje natural para analizar estructuras y categorías gramaticales.

Modelo utilizado:

```text
es_core_news_md
```

### 13.2. Hugging Face

Se utiliza un modelo basado en Transformers para el etiquetado de categorías gramaticales.

Modelo utilizado:

```text
mrm8488/bert-spanish-cased-finetuned-pos
```

### 13.3. Ejecutar la comparación

```bash
python benchmark_nlp.py --out-dir reproduccion_nlp
```

### 13.4. Ejecutar únicamente spaCy

```bash
python benchmark_nlp.py --skip-hf --out-dir reproduccion_spacy
```

### 13.5. Ejecutar únicamente Hugging Face

```bash
python benchmark_nlp.py --skip-spacy --out-dir reproduccion_hf
```

Los archivos generados incluyen:

```text
metrics_nlp_moderno.csv
nlp_detalles.json
```

La ejecución requiere tener instaladas las dependencias y los modelos correspondientes.

---

## 14. Experimentación con modelos LLM

Se realizaron experimentos mediante modelos de lenguaje utilizando dos estrategias de evaluación.

### 14.1. Zero-shot

El modelo recibe instrucciones para clasificar las oraciones sin proporcionar ejemplos previamente resueltos.

### 14.2. Few-shot

El modelo recibe instrucciones y ejemplos resueltos que sirven como referencia para realizar la clasificación.

### 14.3. Configuración de la API

La clave de acceso debe configurarse mediante una variable de entorno.

En PowerShell:

```powershell
$env:GEMINI_API_KEY = "TU_CLAVE"
```

En Git Bash:

```bash
export GEMINI_API_KEY="TU_CLAVE"
```

Para utilizar OpenAI se debe configurar la variable `OPENAI_API_KEY`.

Las claves de API no deben incluirse directamente en el código ni publicarse en GitHub.

### 14.4. Ejecución del experimento

```bash
python llm_experiment.py --provider gemini --model MODELO_DISPONIBLE --version 4 --modos zero-shot few-shot --batch-size 15 --out-dir reproduccion_llm
```

Se debe sustituir `MODELO_DISPONIBLE` por un identificador de modelo válido y disponible en la cuenta utilizada.

### 14.5. Archivos generados

```text
llm_logs.jsonl
metrics_llm.csv
llm_predicciones.json
```

Estos archivos permiten conservar los registros de ejecución, las predicciones y las métricas obtenidas.

Para reproducir los experimentos por bloques de 15 oraciones se pueden utilizar los argumentos `--offset` y `--limit`.

Los registros históricos se encuentran en las siguientes carpetas:

```text
results_batch/
results_batch_2/
results_batch_3/
results_batch_4/
results_batch_few/
results_batch_few_2/
results_batch_few_3/
results_batch_few_4/
```

Los identificadores históricos registrados incluyen `gemini-3.5-flash` y `gemini-3.8-flash`. Su disponibilidad actual debe verificarse antes de reproducir los experimentos.

El archivo `results/llm_logs.jsonl` se encuentra vacío, por lo que deben consultarse los registros almacenados en las carpetas de los bloques experimentales.

La ejecución de modelos mediante API puede generar costos y producir variaciones en las respuestas.

---

## 15. Métricas de evaluación

Para evaluar el rendimiento de los sistemas se utilizaron las siguientes métricas.

### Verdaderos positivos (TP)

Oraciones válidas clasificadas correctamente como válidas.

### Verdaderos negativos (TN)

Oraciones inválidas clasificadas correctamente como inválidas.

### Falsos positivos (FP)

Oraciones inválidas clasificadas incorrectamente como válidas.

### Falsos negativos (FN)

Oraciones válidas clasificadas incorrectamente como inválidas.

### Precisión (Precision)

Representa la proporción de oraciones aceptadas que realmente son válidas.

```text
Precision = TP / (TP + FP)
```

### Recall

Representa la proporción de oraciones válidas que fueron reconocidas correctamente.

```text
Recall = TP / (TP + FN)
```

### Tasa de verdaderos negativos (TNR)

Representa la capacidad del sistema para rechazar oraciones inválidas.

```text
TNR = TN / (TN + FP)
```

### Exactitud (Accuracy)

Representa la proporción total de clasificaciones correctas.

```text
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

### Errores de etiquetado (TagErr)

Representan los errores de etiquetado registrados durante el procesamiento de las oraciones.

---

## 16. Resultados experimentales de las CFG

### 16.1. Resultados globales

| Sistema | Precision | Recall | TNR | Accuracy |
|---|---:|---:|---:|---:|
| CFG v1 | 70.59 % | 24 % | 50 % | 28.33 % |
| CFG v2 | 100 % | 24 % | 100 % | 36.67 % |
| CFG v3 | 100 % | 42 % | 100 % | 51.67 % |
| CFG v4 | 100 % | 64 % | 100 % | 70.00 % |
| CFG v4 + Semántico | 100 % | 52 % | 100 % | 60.00 % |

### 16.2. Matriz de clasificación

| Sistema | TP | TN | FP | FN | TagErr |
|---|---:|---:|---:|---:|---:|
| CFG v1 | 12 | 5 | 5 | 38 | 7 |
| CFG v2 | 12 | 10 | 0 | 38 | 7 |
| CFG v3 | 21 | 10 | 0 | 29 | 7 |
| CFG v4 | 32 | 10 | 0 | 18 | 7 |
| CFG v4 + Semántico | 26 | 10 | 0 | 24 | 7 |

### 16.3. Exactitud por nivel de complejidad

| Sistema | Simple | Intermedio | Complejo |
|---|---:|---:|---:|
| CFG v1 | 65 % | 15 % | 5 % |
| CFG v2 | 90 % | 15 % | 5 % |
| CFG v3 | 90 % | 55 % | 10 % |
| CFG v4 | 90 % | 85 % | 35 % |
| CFG v4 + Semántico | 80 % | 65 % | 35 % |

Los resultados muestran una mejora progresiva en la cobertura de las gramáticas desde CFG v1 hasta CFG v4.

La incorporación del analizador semántico adicional reduce la exactitud global del 70 % al 60 %, debido al rechazo de seis oraciones válidas adicionales.

---

## 17. Comparación general de resultados

| Sistema | Exactitud global |
|---|---:|
| CFG v1 | 28.33 % |
| CFG v2 | 36.67 % |
| CFG v3 | 51.67 % |
| CFG v4 | 70.00 % |
| CFG v4 + Semántico | 60.00 % |
| spaCy | 80.00 % |
| Hugging Face | 83.33 % |
| LLM Zero-shot | 71.67 % |
| LLM Few-shot | 71.67 % |

Hugging Face obtuvo la mayor exactitud global en los resultados históricos. Sin embargo, aceptó las diez oraciones inválidas del conjunto experimental.

spaCy presentó un comportamiento más equilibrado entre la aceptación de oraciones válidas y el rechazo de oraciones inválidas.

Los modelos LLM obtuvieron la misma exactitud global en las estrategias zero-shot y few-shot.

Estos resultados demuestran que la exactitud no debe interpretarse de manera aislada, sino junto con las demás métricas de evaluación.

---

## 18. Reflexión teórica: jerarquía de Chomsky

La jerarquía de Chomsky clasifica las gramáticas formales según su capacidad expresiva.

| Tipo | Gramática | Modelo computacional |
|---|---|---|
| Tipo 0 | Gramáticas irrestrictas | Máquina de Turing |
| Tipo 1 | Gramáticas sensibles al contexto | Autómata linealmente acotado |
| Tipo 2 | Gramáticas libres de contexto | Autómata de pila |
| Tipo 3 | Gramáticas regulares | Autómata finito |

Las gramáticas libres de contexto permiten representar estructuras sintácticas anidadas, recursividad y diferentes árboles de derivación.

Sin embargo, determinados fenómenos del lenguaje natural requieren relacionar información entre diferentes elementos de una oración.

La concordancia, las dependencias cruzadas y la interpretación contextual pueden aumentar considerablemente la complejidad de una implementación basada en reglas.

El incremento de reglas desde CFG v1 hasta CFG v4 evidencia el esfuerzo necesario para ampliar la cobertura del subconjunto del español estudiado.

No obstante, el crecimiento de las reglas por sí solo no demuestra formalmente que un lenguaje no sea libre de contexto.

---

## 19. Limitaciones identificadas

### Limitaciones léxicas

El vocabulario definido es reducido, por lo que algunas oraciones válidas pueden ser rechazadas al contener palabras no contempladas.

### Concordancia gramatical

La incorporación de restricciones de género, número y persona incrementa la complejidad de las reglas.

### Ambigüedad

Una misma oración puede generar múltiples árboles sintácticos. La gramática representa las interpretaciones posibles, pero no necesariamente determina cuál corresponde a la intención del hablante.

### Recursividad

Las estructuras subordinadas permiten representar oraciones anidadas, aunque la complejidad del análisis puede aumentar conforme se amplían las estructuras.

### Dependencias cruzadas

Algunas relaciones entre elementos distantes requieren mecanismos adicionales para controlar la compatibilidad entre símbolos.

### Análisis semántico

Las restricciones adicionales pueden producir falsos negativos cuando son demasiado rígidas.

### Herramientas NLP y LLM

Los resultados dependen de los modelos utilizados, las heurísticas de clasificación, las instrucciones proporcionadas y las características del conjunto experimental.

---

## 20. Verificación de reproducibilidad

El 25 de noviembre de 2026 se realizó una nueva ejecución de las gramáticas mediante el comando:

```bash
python eval_cfg.py --out-dir reproduccion_cfg
```

Se verificó que los resultados globales coinciden con las métricas originales del informe final.

| Sistema | Resultado original | Resultado reproducido |
|---|---:|---:|
| CFG v1 | 28.33 % | 28.33 % |
| CFG v2 | 36.67 % | 36.67 % |
| CFG v3 | 51.67 % | 51.67 % |
| CFG v4 | 70.00 % | 70.00 % |
| CFG v4 + Semántico | 60.00 % | 60.00 % |

También se verificó el funcionamiento de la visualización gráfica utilizando:

- Windows.
- Python 3.12.
- NLTK 3.10.4.
- Tkinter 8.6.

Las modificaciones realizadas en `prueba-es.py` no alteraron los resultados experimentales de las gramáticas.

Los resultados de spaCy, Hugging Face y LLM corresponden a las evidencias históricas almacenadas en el repositorio. Su nueva ejecución queda pendiente de verificación.

---

## 21. Actualizaciones realizadas

Se incorporaron las siguientes mejoras:

- Documentación completa de la Fase 2.
- Corrección del conteo de respuestas correctas en el reporte de `prueba-es.py`.
- Incorporación del argumento opcional `--grafico`.
- Visualización gráfica de árboles mediante NLTK.
- Manejo de errores relacionados con las dependencias gráficas.
- Verificación de la generación de árboles sintácticos.
- Comprobación de la ambigüedad mediante múltiples árboles.
- Reproducción de las métricas de las 60 oraciones.
- Documentación de los comandos necesarios para reproducir los experimentos.

Estas modificaciones no alteran las cuatro versiones de la gramática ni la lógica del analizador sintáctico y semántico.

---

## 22. Relación entre la Fase 1 y la Fase 2

En la primera fase se desarrolló un analizador para un subconjunto del lenguaje de programación C++, incorporando análisis léxico, sintáctico y semántico.

En la segunda fase se aplicaron conceptos similares al procesamiento de un subconjunto del lenguaje español.

La comparación permite identificar diferencias entre los lenguajes de programación y los lenguajes naturales.

Mientras que los lenguajes de programación poseen reglas estructurales y semánticas definidas, los lenguajes naturales presentan fenómenos adicionales como ambigüedad, variabilidad e interpretación contextual.

Ambas fases permiten estudiar las capacidades y limitaciones de los modelos formales de la jerarquía de Chomsky.

---

## 23. Conclusiones

El desarrollo incremental de las gramáticas permitió ampliar progresivamente la cobertura sintáctica del subconjunto del español estudiado.

La cuarta versión obtuvo una exactitud del 70 %, superando los resultados de las versiones anteriores.

La incorporación de verificaciones semánticas adicionales redujo la exactitud al 60 %, demostrando que agregar restricciones no garantiza necesariamente una mejora en el rendimiento.

La comparación con herramientas modernas de NLP y modelos LLM permitió identificar diferentes comportamientos y limitaciones en la clasificación de oraciones.

Los resultados evidencian que ninguna de las configuraciones evaluadas resuelve correctamente todos los casos del conjunto experimental.

Finalmente, el proyecto permitió relacionar los fundamentos teóricos de las gramáticas formales y la jerarquía de Chomsky con aplicaciones prácticas del procesamiento del lenguaje natural.

---

**Universidad Centroamericana José Simeón Cañas (UCA)**

**Teoría de Programación — Ciclo 02-2026**

**Proyecto TLP02-2026 — Fase 2**