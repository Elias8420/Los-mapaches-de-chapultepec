import argparse
import json
from pathlib import Path
from typing import Any

from metrics import calcular_metricas, guardar_resumen_csv


def cargar_dataset(ruta: str | Path) -> list[dict]:
    with Path(ruta).open(encoding="utf-8") as f:
        return json.load(f)


# =====================================================================
# 1. Evaluador con spaCy
# =====================================================================
def evaluar_spacy(dataset: list[dict], modelo_spacy: str = "es_core_news_md") -> tuple[list[dict], list[dict]]:
    import spacy

    nlp = spacy.load(modelo_spacy)
    registros = []
    detalles = []

    for item in dataset:
        texto = item["texto"]
        doc = nlp(texto)

        tokens_info = []
        tiene_dep_vacia = False
        tiene_pos_desconocido = False
        tiene_dep_sin_clasificar = False
        tiene_root_verbal = False

        # Revisar estructura básica de dependencias y POS
        for tok in doc:
            if tok.is_space or tok.is_punct:
                continue
            pos = tok.pos_
            dep = tok.dep_
            morph = tok.morph.to_dict()

            if not pos or pos == "X":
                tiene_pos_desconocido = True
            if not dep:
                tiene_dep_vacia = True
            if dep == "dep":
                tiene_dep_sin_clasificar = True
            if dep == "ROOT" and pos in ("VERB", "AUX"):
                tiene_root_verbal = True

            tokens_info.append({
                "texto": tok.text,
                "pos": pos,
                "dep": dep,
                "head": tok.head.text,
                "morph": morph,
            })

        # Heurística de concordancia morfosintáctica detectada por spaCy
        error_conc_spacy = _detectar_discordancia_spacy(doc)

        # Predicción: acepta estructuralmente si hay núcleo verbal y no hay dependencias rotas
        pred_valida = bool(
            len(tokens_info) > 0
            and tiene_root_verbal
            and not tiene_dep_vacia
            and not error_conc_spacy
        )
        error_etiquetado = bool(
            tiene_pos_desconocido
            or tiene_dep_sin_clasificar
            or error_conc_spacy
        )

        rec = {
            "id": item["id"],
            "nivel": item["nivel"],
            "fenomeno": item["fenomeno"],
            "texto": texto,
            "esperado_valido": bool(item["esperado_valido"]),
            "pred_valida": pred_valida,
            "error_etiquetado": error_etiquetado,
        }
        registros.append(rec)
        detalles.append({**rec, "modelo": modelo_spacy, "tokens": tokens_info})

    return registros, detalles


def _detectar_discordancia_spacy(doc) -> bool:
    """Busca discordancias obvias de género/número/persona en dependencias de spaCy."""
    for tok in doc:
        if tok.is_space or tok.is_punct:
            continue
        m_tok = tok.morph.to_dict()
        m_head = tok.head.morph.to_dict()

        # Determinantes / modificadores nominales vs cabeza nominal
        if tok.dep_ in ("det", "amod") and tok.head.pos_ in ("NOUN", "PROPN"):
            if "Gender" in m_tok and "Gender" in m_head and m_tok["Gender"] != m_head["Gender"]:
                return True
            if "Number" in m_tok and "Number" in m_head and m_tok["Number"] != m_head["Number"]:
                return True

        # Sujeto nominal/pronominal vs verbo cabeza
        if tok.dep_ in ("nsubj", "nsubj:pass") and tok.head.pos_ in ("VERB", "AUX"):
            if "Number" in m_tok and "Number" in m_head and m_tok["Number"] != m_head["Number"]:
                return True
            if "Person" in m_tok and "Person" in m_head and m_tok["Person"] != m_head["Person"]:
                return True

    return False


# =====================================================================
# 2. Evaluador con HuggingFace Transformers
# =====================================================================
def evaluar_huggingface(
    dataset: list[dict],
    modelo_hf: str = "mrm8488/bert-spanish-cased-finetuned-pos",
    umbral_confianza: float = 0.65,
) -> tuple[list[dict], list[dict]]:
    from transformers import pipeline

    ner_pos = pipeline(
        "token-classification",
        model=modelo_hf,
        tokenizer=modelo_hf,
        aggregation_strategy="simple",
    )

    registros = []
    detalles = []

    for item in dataset:
        texto = item["texto"]
        salida_hf = ner_pos(texto)

        etiquetas_pred = []
        baja_confianza = False
        etiqueta_invalida = False

        for ent in salida_hf:
            et = str(ent.get("entity_group", ent.get("entity", "")))
            score = float(ent.get("score", 0.0))
            palabra = str(ent.get("word", "")).strip()

            if score < umbral_confianza:
                baja_confianza = True
            if not et or et.upper() in {"UNK", "X", "O"}:
                etiqueta_invalida = True

            etiquetas_pred.append({
                "palabra": palabra,
                "etiqueta": et,
                "score": round(score, 4),
            })

        # Criterio estructural mínimo: al menos un verbo/predicado identificado y sin fallos graves
        tiene_verbo = any(
            e["etiqueta"].upper().startswith(("V", "VERB", "AUX"))
            for e in etiquetas_pred
        )
        pred_valida = bool(len(etiquetas_pred) > 0 and tiene_verbo and not etiqueta_invalida)
        error_etiquetado = bool(baja_confianza or etiqueta_invalida)

        rec = {
            "id": item["id"],
            "nivel": item["nivel"],
            "fenomeno": item["fenomeno"],
            "texto": texto,
            "esperado_valido": bool(item["esperado_valido"]),
            "pred_valida": pred_valida,
            "error_etiquetado": error_etiquetado,
        }
        registros.append(rec)
        detalles.append({**rec, "modelo": modelo_hf, "predicciones_hf": etiquetas_pred})

    return registros, detalles


# =====================================================================
# 3. Reporte y exportación
# =====================================================================
def construir_filas_resumen(nombre_sistema: str, registros: list[dict]) -> list[dict]:
    filas = []
    global_m = calcular_metricas(registros)
    filas.append({"sistema": nombre_sistema, "nivel": "GLOBAL", **global_m})

    for nivel in ("1_simple", "2_intermedio", "3_complejo"):
        sub = [r for r in registros if r["nivel"] == nivel]
        m = calcular_metricas(sub)
        filas.append({"sistema": nombre_sistema, "nivel": nivel, **m})
    return filas


def imprimir_tabla_resumen(filas: list[dict]) -> None:
    print(
        f"{'Sistema':<22} {'Nivel':<14} {'Prec':>7} {'Rec':>7} {'TNR':>7} "
        f"{'Acc':>7} {'TP':>4} {'TN':>4} {'FP':>4} {'FN':>4} {'TagErr':>7}"
    )
    print("-" * 102)
    for f in filas:
        print(
            f"{f['sistema']:<22} {f['nivel']:<14} "
            f"{f['precision']:>7.2f} {f['cobertura_recall']:>7.2f} {f['tasa_rechazo_correcto']:>7.2f} "
            f"{f['exactitud']:>7.2f} {f['TP']:>4} {f['TN']:>4} {f['FP']:>4} {f['FN']:>4} "
            f"{f['errores_etiquetado']:>7}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Evalúa el set de prueba con spaCy y HuggingFace.")
    parser.add_argument("--dataset", default="data/test_set_60.json", help="Ruta al JSON del dataset")
    parser.add_argument("--spacy-model", default="es_core_news_md", help="Modelo de spaCy en español")
    parser.add_argument(
        "--hf-model",
        default="mrm8488/bert-spanish-cased-finetuned-pos",
        help="Modelo de HuggingFace para token-classification / POS",
    )
    parser.add_argument("--skip-spacy", action="store_true", help="Omitir spaCy")
    parser.add_argument("--skip-hf", action="store_true", help="Omitir HuggingFace")
    parser.add_argument("--out-dir", default="results", help="Directorio de salida")
    args = parser.parse_args()

    dataset = cargar_dataset(args.dataset)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    todas_las_filas: list[dict] = []
    detalles_completos: dict[str, Any] = {}

    if not args.skip_spacy:
        try:
            reg_spacy, det_spacy = evaluar_spacy(dataset, args.spacy_model)
            filas_s = construir_filas_resumen(f"spaCy ({args.spacy_model})", reg_spacy)
            todas_las_filas.extend(filas_s)
            detalles_completos["spacy"] = det_spacy
        except Exception as e:
            print(f"[Aviso] No se pudo ejecutar spaCy ({args.spacy_model}): {e}")

    if not args.skip_hf:
        try:
            reg_hf, det_hf = evaluar_huggingface(dataset, args.hf_model)
            filas_h = construir_filas_resumen(f"HF ({args.hf_model.split('/')[-1]})", reg_hf)
            todas_las_filas.extend(filas_h)
            detalles_completos["huggingface"] = det_hf
        except Exception as e:
            print(f"[Aviso] No se pudo ejecutar HuggingFace ({args.hf_model}): {e}")

    if todas_las_filas:
        print("\n=== Resumen cuantitativo NLP moderno ===")
        imprimir_tabla_resumen(todas_las_filas)
        guardar_resumen_csv(todas_las_filas, out_dir / "metrics_nlp_moderno.csv")
        with (out_dir / "nlp_detalles.json").open("w", encoding="utf-8") as f:
            json.dump(detalles_completos, f, ensure_ascii=False, indent=2)
        print(f"\nGuardado en: {out_dir / 'metrics_nlp_moderno.csv'} y {out_dir / 'nlp_detalles.json'}")
    else:
        print("No se generó ninguna fila de métricas. Verifica los modelos instalados.")


if __name__ == "__main__":
    main()