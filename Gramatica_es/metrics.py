import csv
from pathlib import Path
from typing import Iterable


def calcular_metricas(registros: Iterable[dict]) -> dict:
    tp = tn = fp = fn = tag_errors = 0
    total = 0

    for r in registros:
        total += 1
        esp = bool(r["esperado_valido"])
        pred = bool(r["pred_valida"])
        if r.get("error_etiquetado", False):
            tag_errors += 1

        if esp and pred:
            tp += 1
        elif not esp and not pred:
            tn += 1
        elif not esp and pred:
            fp += 1
        elif esp and not pred:
            fn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    tnr = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    accuracy = (tp + tn) / total if total > 0 else 0.0

    return {
        "total": total,
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "errores_etiquetado": tag_errors,
        "precision": round(precision, 4),
        "cobertura_recall": round(recall, 4),
        "tasa_rechazo_correcto": round(tnr, 4),
        "exactitud": round(accuracy, 4),
    }


def evaluar_parser(parser, dataset: list[dict], error_lexico_cls=Exception, semantico=None) -> list[dict]:
    salida = []
    for item in dataset:
        texto = item["texto"]
        tag_err = False
        try:
            arboles = parser.analizar(texto)
            if not arboles:
                pred_valida = False
            elif semantico is not None:
                # Válida si al menos un árbol pasa la validación semántica
                pred_valida = any(semantico.validar_texto(texto, arb)[0] for arb in arboles)
            else:
                pred_valida = True
        except error_lexico_cls:
            pred_valida = False
            tag_err = True

        salida.append({
            "id": item["id"],
            "nivel": item["nivel"],
            "fenomeno": item["fenomeno"],
            "texto": texto,
            "esperado_valido": item["esperado_valido"],
            "pred_valida": pred_valida,
            "error_etiquetado": tag_err,
        })
    return salida


def guardar_resumen_csv(filas: list[dict], ruta_csv: str | Path) -> None:
    ruta = Path(ruta_csv)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    if not filas:
        return
    with ruta.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        writer.writeheader()
        writer.writerows(filas)