import argparse
import json
import os
import re
import time
from pathlib import Path
from typing import Any

from gramaticas_es import VERSIONES, contar_lexicas
from metrics import calcular_metricas, guardar_resumen_csv


def cargar_dataset(ruta: str | Path) -> list[dict]:
    with Path(ruta).open(encoding="utf-8") as f:
        return json.load(f)


def formatear_reglas_cfg(version: int = 4) -> str:
    """Convierte las reglas formales de VERSIONES[version] y sus preterminales a texto."""
    nombre, g_fn, e_fn = VERSIONES[version]
    reglas = g_fn()
    no_terminales = set(reglas.keys())
    preterminales = set()
    lineas_reglas = []

    for nt, alts in reglas.items():
        for sim in alts:
            for s in sim:
                if s not in no_terminales:
                    preterminales.add(s)
        cuerpo = " | ".join(" ".join(sim) if sim else "ε" for sim in alts)
        lineas_reglas.append(f"  {nt} -> {cuerpo}")

    rl, cl = contar_lexicas(e_fn)
    cats_ordenadas = ", ".join(sorted(preterminales))
    return (
        f"Gramática formal ({nombre}):\n"
        f"Símbolo inicial: O\n"
        f"Preterminales en reglas ({len(preterminales)}): {cats_ordenadas}\n"
        f"Léxico asociado: {rl} entradas en {cl} categorías léxicas\n"
        f"Producciones:\n" + "\n".join(lineas_reglas)
    )


def _bloque_base_y_ejemplos(reglas_texto: str, modo: str) -> str:
    base = (
        "Eres un evaluador estricto de una Gramática Libre de Contexto (CFG) formal para un subconjunto del español.\n"
        "Debes decidir si cada oración es ACEPTADA o RECHAZADA *exclusivamente* bajo las reglas formales indicadas, "
        "NO según tu conocimiento general del español natural.\n"
        "- 'aceptada': true solo si la oración se deriva completamente desde O usando las reglas y categorías dadas.\n"
        "- 'error_etiquetado': true si hay palabras fuera de las categorías/léxico esperado o ambigüedad/fallo de clasificación.\n\n"
        f"{reglas_texto}\n"
    )
    if modo == "few-shot":
        base += (
            "\nEjemplos de evaluación formal:\n"
            '1) Oración: "el gato come el pescado"\n'
            '   Respuesta: {"aceptada": true, "error_etiquetado": false, "motivo": "Derivable en O -> SNs_3s SV_3s con concordancia."}\n'
            '2) Oración: "la gato come el pescado"\n'
            '   Respuesta: {"aceptada": false, "error_etiquetado": false, "motivo": "Discordancia de género/número en SN_fs."}\n'
            '3) Oración: "comemos el pescado"\n'
            '   Respuesta: {"aceptada": false, "error_etiquetado": false, "motivo": "Las reglas de O requieren SNs explícito antes de SV."}\n'
            '4) Oración: "el gato come la zanahoria"\n'
            '   Respuesta: {"aceptada": false, "error_etiquetado": true, "motivo": "zanahoria no pertenece al léxico/categorías definidas."}\n'
        )
    return base


def construir_prompt(oracion: str, reglas_texto: str, modo: str) -> str:
    instrucciones = (
        _bloque_base_y_ejemplos(reglas_texto, modo)
        + "\nResponde ÚNICAMENTE con un objeto JSON válido con estas claves:\n"
        '{"aceptada": true/false, "error_etiquetado": true/false, "motivo": "explicación breve"}\n'
    )
    return f"{instrucciones}\nOración a evaluar: {oracion!r}\nJSON:"


def construir_prompt_lote(lote: list[dict], reglas_texto: str, modo: str) -> str:
    lineas_oraciones = "\n".join(f'- id: "{item["id"]}" | texto: {item["texto"]!r}' for item in lote)
    instrucciones = (
        _bloque_base_y_ejemplos(reglas_texto, modo)
        + "\nEvalúa cada oración de forma independiente y responde ÚNICAMENTE con un arreglo JSON válido "
        "(sin texto extra ni bloques markdown) con un objeto por oración usando estas claves:\n"
        '[{"id": "...", "aceptada": true/false, "error_etiquetado": true/false, "motivo": "explicación breve"}]\n'
    )
    return f"{instrucciones}\nOraciones a evaluar ({len(lote)}):\n{lineas_oraciones}\nJSON:"


def llamar_llm(prompt: str, provider: str, model: str, max_reintentos: int = 3) -> str:
    if provider == "gemini":
        from google import genai

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("Falta la variable de entorno GEMINI_API_KEY.")
        client = genai.Client(api_key=api_key)

        for intento in range(1, max_reintentos + 1):
            try:
                resp = client.models.generate_content(model=model, contents=prompt)
                return resp.text or ""
            except Exception as exc:
                msg = str(exc)
                if "limit: 0" in msg or "QuotaFailure" in msg:
                    raise
                es_transitorio = (
                    any(tok in msg for tok in ("503", "UNAVAILABLE", "10053", "ReadError", "ConnectionError"))
                    or ("429" in msg and intento < max_reintentos)
                )
                if not es_transitorio or intento == max_reintentos:
                    raise
                espera = 2 ** intento
                print(f"[Aviso] Error transitorio ({intento}/{max_reintentos}), reintentando en {espera}s...")
                time.sleep(espera)

    if provider == "openai":
        from openai import OpenAI

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Falta la variable de entorno OPENAI_API_KEY.")
        client = OpenAI(api_key=api_key)

        for intento in range(1, max_reintentos + 1):
            try:
                resp = client.chat.completions.create(
                    model=model,
                    temperature=0,
                    messages=[{"role": "user", "content": prompt}],
                )
                return resp.choices[0].message.content or ""
            except Exception as exc:
                msg = str(exc)
                es_transitorio = (
                    any(tok in msg for tok in ("503", "429", "10053", "ReadError", "ConnectionError"))
                    or ("rate_limit" in msg.lower() and intento < max_reintentos)
                )
                if not es_transitorio or intento == max_reintentos:
                    raise
                espera = 2 ** intento
                print(f"[Aviso] Error transitorio OpenAI ({intento}/{max_reintentos}), reintentando en {espera}s...")
                time.sleep(espera)

    raise ValueError(f"Proveedor no soportado: {provider}")


def _limpiar_texto_json(texto_resp: str) -> str:
    limpio = texto_resp.strip()
    limpio = re.sub(r"^```(?:json)?\s*|\s*```$", "", limpio, flags=re.IGNORECASE | re.MULTILINE).strip()
    return limpio


def parsear_respuesta_llm(texto_resp: str) -> tuple[bool, bool, str, bool]:
    """Devuelve (aceptada, error_etiquetado, motivo, parseo_ok)."""
    limpio = _limpiar_texto_json(texto_resp)
    match = re.search(r"\{.*\}", limpio, flags=re.DOTALL)
    candidato = match.group(0) if match else limpio

    try:
        data = json.loads(candidato)
        if isinstance(data, list) and data:
            data = data[0]
        aceptada = bool(data.get("aceptada", False))
        err_tag = bool(data.get("error_etiquetado", False))
        motivo = str(data.get("motivo", ""))
        return aceptada, err_tag, motivo, True
    except Exception:
        baja = limpio.lower()
        aceptada = ('"aceptada": true' in baja) or ("aceptada: true" in baja)
        return aceptada, True, f"Respuesta no-JSON: {limpio[:160]}", False


def parsear_respuesta_lote(texto_resp: str, lote: list[dict]) -> list[tuple[bool, bool, str, bool]]:
    """Devuelve una lista alineada con `lote` de tuplas (aceptada, error_etiquetado, motivo, parseo_ok)."""
    limpio = _limpiar_texto_json(texto_resp)
    match_arr = re.search(r"\[.*\]", limpio, flags=re.DOTALL)
    candidato = match_arr.group(0) if match_arr else limpio

    elementos: list[dict] = []
    parseo_global_ok = False
    try:
        parsed = json.loads(candidato)
        if isinstance(parsed, list):
            elementos = [x for x in parsed if isinstance(x, dict)]
            parseo_global_ok = len(elementos) == len(lote)
        elif isinstance(parsed, dict) and len(lote) == 1:
            elementos = [parsed]
            parseo_global_ok = True
    except Exception:
        parseo_global_ok = False

    por_id = {str(obj.get("id", "")).strip(): obj for obj in elementos if obj.get("id") is not None}
    resultados: list[tuple[bool, bool, str, bool]] = []

    for idx, item in enumerate(lote):
        item_id = str(item["id"])
        obj = por_id.get(item_id)
        if obj is None and idx < len(elementos):
            obj = elementos[idx]

        if obj is not None:
            aceptada = bool(obj.get("aceptada", False))
            err_tag = bool(obj.get("error_etiquetado", False))
            motivo = str(obj.get("motivo", ""))
            ok = parseo_global_ok or (str(obj.get("id", "")).strip() == item_id)
            resultados.append((aceptada, err_tag, motivo, ok))
        else:
            resultados.append((False, True, f"Elemento faltante en lote para id={item_id}: {limpio[:120]}", False))

    return resultados


def construir_filas_resumen(nombre_sistema: str, registros: list[dict]) -> list[dict]:
    filas = [{"sistema": nombre_sistema, "nivel": "GLOBAL", **calcular_metricas(registros)}]
    for nivel in ("1_simple", "2_intermedio", "3_complejo"):
        sub = [r for r in registros if r["nivel"] == nivel]
        filas.append({"sistema": nombre_sistema, "nivel": nivel, **calcular_metricas(sub)})
    return filas


def imprimir_tabla(filas: list[dict]) -> None:
    print(
        f"{'Sistema':<28} {'Nivel':<14} {'Prec':>7} {'Rec':>7} {'TNR':>7} "
        f"{'Acc':>7} {'TP':>4} {'TN':>4} {'FP':>4} {'FN':>4} {'TagErr':>7}"
    )
    print("-" * 108)
    for f in filas:
        print(
            f"{f['sistema']:<28} {f['nivel']:<14} "
            f"{f['precision']:>7.2f} {f['cobertura_recall']:>7.2f} {f['tasa_rechazo_correcto']:>7.2f} "
            f"{f['exactitud']:>7.2f} {f['TP']:>4} {f['TN']:>4} {f['FP']:>4} {f['FN']:>4} "
            f"{f['errores_etiquetado']:>7}"
        )


def main() -> None:
    ap = argparse.ArgumentParser(description="Experimento LLM zero-shot vs few-shot con reglas CFG.")
    ap.add_argument("--dataset", default="data/test_set_60.json")
    ap.add_argument("--version", type=int, default=4, choices=sorted(VERSIONES.keys()))
    ap.add_argument("--provider", default="gemini", choices=["gemini", "openai"])
    ap.add_argument("--model", default="gemini-4-carbon")
    ap.add_argument("--modos", nargs="+", default=["zero-shot", "few-shot"], choices=["zero-shot", "few-shot"])
    ap.add_argument("--batch-size", type=int, default=1, help="Cantidad de oraciones por llamada a la API.")
    ap.add_argument("--offset", type=int, default=0, help="Índice inicial dentro del dataset.")
    ap.add_argument("--limit", type=int, default=None, help="Limita el número de oraciones por modo.")
    ap.add_argument("--sleep", type=float, default=0.0, help="Pausa en segundos entre llamadas a la API.")
    ap.add_argument("--append", action="store_true", help="Agrega a llm_logs.jsonl en vez de sobrescribir.")
    ap.add_argument("--out-dir", default="results")
    args = ap.parse_args()

    if args.batch_size < 1:
        raise ValueError("--batch-size debe ser mayor o igual a 1.")
    if args.offset < 0:
        raise ValueError("--offset debe ser mayor o igual a 0.")

    dataset = cargar_dataset(args.dataset)
    if args.offset:
        dataset = dataset[args.offset :]
    if args.limit is not None:
        dataset = dataset[: args.limit]

    reglas_texto = formatear_reglas_cfg(args.version)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    log_path = out_dir / "llm_logs.jsonl"
    modo_apertura = "a" if args.append else "w"

    todas_filas: list[dict] = []
    resumen_json: dict[str, Any] = {}

    with log_path.open(modo_apertura, encoding="utf-8") as log_file:
        for modo in args.modos:
            registros_modo: list[dict] = []
            lotes = [dataset[i : i + args.batch_size] for i in range(0, len(dataset), args.batch_size)]

            for idx_lote, lote in enumerate(lotes):
                if args.batch_size == 1:
                    item = lote[0]
                    prompt = construir_prompt(item["texto"], reglas_texto, modo=modo)
                    raw_resp = llamar_llm(prompt, provider=args.provider, model=args.model)
                    parsed_items = [parsear_respuesta_llm(raw_resp)]
                else:
                    prompt = construir_prompt_lote(lote, reglas_texto, modo=modo)
                    raw_resp = llamar_llm(prompt, provider=args.provider, model=args.model)
                    parsed_items = parsear_respuesta_lote(raw_resp, lote)

                for item, (aceptada, err_tag, motivo, parseo_ok) in zip(lote, parsed_items):
                    reg = {
                        "id": item["id"],
                        "nivel": item["nivel"],
                        "fenomeno": item["fenomeno"],
                        "texto": item["texto"],
                        "esperado_valido": bool(item["esperado_valido"]),
                        "pred_valida": aceptada,
                        "error_etiquetado": bool(err_tag or not parseo_ok),
                    }
                    registros_modo.append(reg)

                    evento_log = {
                        "provider": args.provider,
                        "model": args.model,
                        "cfg_version": args.version,
                        "modo": modo,
                        "batch_size": args.batch_size,
                        "batch_index": idx_lote,
                        "item": item,
                        "prompt": prompt,
                        "raw_response": raw_resp,
                        "parsed": {
                            "aceptada": aceptada,
                            "error_etiquetado": err_tag,
                            "motivo": motivo,
                            "parseo_ok": parseo_ok,
                        },
                        "metric_record": reg,
                    }
                    log_file.write(json.dumps(evento_log, ensure_ascii=False) + "\n")

                log_file.flush()

                if args.sleep > 0 and idx_lote < len(lotes) - 1:
                    time.sleep(args.sleep)

            nombre_sis = f"LLM_{modo} ({args.model})"
            todas_filas.extend(construir_filas_resumen(nombre_sis, registros_modo))
            resumen_json[nombre_sis] = registros_modo

    print("\n=== Resumen cuantitativo LLM (zero-shot vs few-shot) ===")
    imprimir_tabla(todas_filas)

    guardar_resumen_csv(todas_filas, out_dir / "metrics_llm.csv")
    with (out_dir / "llm_predicciones.json").open("w", encoding="utf-8") as f:
        json.dump(resumen_json, f, ensure_ascii=False, indent=2)

    print(f"\nLogs guardados en: {log_path}")
    print(f"Métricas guardadas en: {out_dir / 'metrics_llm.csv'}")


if __name__ == "__main__":
    main()