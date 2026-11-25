import argparse
import json
from pathlib import Path
from typing import Any

from gramaticas_es import VERSIONES
from lexico import ErrorLexicoES
from metrics import calcular_metricas, evaluar_parser, guardar_resumen_csv
from parser_es import ParserGramatica
from semantico import AnalizadorSemanticoES


def cargar_dataset(ruta: str | Path) -> list[dict]:
    with Path(ruta).open(encoding="utf-8") as f:
        return json.load(f)


def construir_filas(nombre_sistema: str, registros: list[dict]) -> list[dict]:
    filas = []
    m_global = calcular_metricas(registros)
    filas.append({"sistema": nombre_sistema, "nivel": "GLOBAL", **m_global})

    for nivel in ("1_simple", "2_intermedio", "3_complejo"):
        sub = [r for r in registros if r["nivel"] == nivel]
        m_niv = calcular_metricas(sub)
        filas.append({"sistema": nombre_sistema, "nivel": nivel, **m_niv})
    return filas


def imprimir_tabla(filas: list[dict]) -> None:
    print(
        f"{'Sistema':<24} {'Nivel':<14} {'Prec':>7} {'Rec':>7} {'TNR':>7} "
        f"{'Acc':>7} {'TP':>4} {'TN':>4} {'FP':>4} {'FN':>4} {'TagErr':>7}"
    )
    print("-" * 104)
    for f in filas:
        print(
            f"{f['sistema']:<24} {f['nivel']:<14} "
            f"{f['precision']:>7.2f} {f['cobertura_recall']:>7.2f} {f['tasa_rechazo_correcto']:>7.2f} "
            f"{f['exactitud']:>7.2f} {f['TP']:>4} {f['TN']:>4} {f['FP']:>4} {f['FN']:>4} "
            f"{f['errores_etiquetado']:>7}"
        )


def main() -> None:
    ap = argparse.ArgumentParser(description="Evalúa v1-v4 y v4+semántico sobre las 60 oraciones.")
    ap.add_argument("--dataset", default="data/test_set_60.json")
    ap.add_argument("--out-dir", default="results")
    args = ap.parse_args()

    dataset = cargar_dataset(args.dataset)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    todas_filas: list[dict] = []
    detalles: dict[str, Any] = {}
    sem = AnalizadorSemanticoES()

    for v, (nombre, g_fn, e_fn) in sorted(VERSIONES.items()):
        parser = ParserGramatica(g_fn(), e_fn)
        regs = evaluar_parser(parser, dataset, ErrorLexicoES, semantico=None)
        nombre_sis = f"CFG_v{v}"
        todas_filas.extend(construir_filas(nombre_sis, regs))
        detalles[nombre_sis] = {"descripcion": nombre, "registros": regs}

        # En v4 también evaluamos el contraste con el analizador semántico
        if v == 4:
            regs_sem = evaluar_parser(parser, dataset, ErrorLexicoES, semantico=sem)
            nombre_sem = "CFG_v4+Semantico"
            todas_filas.extend(construir_filas(nombre_sem, regs_sem))
            detalles[nombre_sem] = {
                "descripcion": f"{nombre} + AnalizadorSemanticoES",
                "registros": regs_sem,
            }

    print("=== Métricas CFG (v1-v4) y v4 + Semántico sobre 60 oraciones ===")
    imprimir_tabla(todas_filas)

    csv_path = out_dir / "metrics_cfg_60.csv"
    json_path = out_dir / "cfg_detalles.json"
    guardar_resumen_csv(todas_filas, csv_path)
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(detalles, f, ensure_ascii=False, indent=2)

    print(f"\nGuardado en: {csv_path} y {json_path}")


if __name__ == "__main__":
    main()