from lexico import LEXICO, tokenizar_es, ErrorLexicoES
from tree import Nodo


class AnalizadorSemanticoES:
    """
    Valida concordancia morfosintáctica (género, número, persona y modo verbal)
    sobre un árbol `Nodo` producido por `ParserGramatica`.
    Retorna (es_valido: bool, errores: list[str]).
    """

    def __init__(self, lexico: dict = LEXICO):
        self.lexico = lexico

    def validar_texto(self, texto: str, arbol: Nodo) -> tuple[bool, list[str]]:
        try:
            tokens = tokenizar_es(texto)
        except ErrorLexicoES as e:
            return False, [str(e)]
        return self.validar_arbol(arbol, tokens)

    def validar_arbol(self, arbol: Nodo, tokens: list | None = None) -> tuple[bool, list[str]]:
        errores: list[str] = []
        hojas = self._hojas(arbol)

        # Asociar cada hoja léxica con sus posibles análisis en LEXICO
        hojas_con_rasgos = []
        for idx, hoja in enumerate(hojas):
            palabra = (hoja.valor or "").lower()
            analisis_posibles = []
            if tokens and idx < len(tokens) and tokens[idx].texto == palabra:
                analisis_posibles = tokens[idx].analisis
            elif palabra in self.lexico:
                analisis_posibles = self.lexico[palabra]
            hojas_con_rasgos.append((hoja, analisis_posibles))

        self._chequear_nodo(arbol, hojas_con_rasgos, errores)
        return len(errores) == 0, errores

    def _hojas(self, nodo: Nodo) -> list[Nodo]:
        if not nodo.hijos:
            return [nodo] if nodo.valor is not None else []
        out = []
        for h in nodo.hijos:
            out.extend(self._hojas(h))
        return out

    def _rasgos_en_subarbol(self, nodo: Nodo, hojas_con_rasgos: list) -> list[dict]:
        hojas_sub = set(id(h) for h in self._hojas(nodo))
        rasgos = []
        for hoja, lecturas in hojas_con_rasgos:
            if id(hoja) in hojas_sub and lecturas:
                # Si la hoja tiene etiqueta específica como Vt_3s o Det_ms, filtramos lecturas compatibles
                filtradas = [
                    r for r in lecturas
                    if self._coincide_etiqueta_hoja(hoja.etiqueta, r)
                ]
                rasgos.extend(filtradas or lecturas)
        return rasgos

    def _coincide_etiqueta_hoja(self, et_hoja: str, r: dict) -> bool:
        cat = r.get("cat", "")
        if et_hoja == cat:
            return True
        if et_hoja.startswith(cat + "_"):
            return True
        if cat == "V" and et_hoja.startswith("V" + str(r.get("sub", ""))):
            return True
        return False

    def _compatibles(self, v1, v2) -> bool:
        if v1 is None or v2 is None:
            return True
        s1 = set(v1) if isinstance(v1, (tuple, list, set)) else {v1}
        s2 = set(v2) if isinstance(v2, (tuple, list, set)) else {v2}
        return len(s1 & s2) > 0

    def _chequear_nodo(self, nodo: Nodo, hojas_con_rasgos: list, errores: list[str]) -> None:
        # 1. Concordancia de género y número en sintagmas nominales / grupos adjetivales
        if nodo.etiqueta.startswith("SN") or nodo.etiqueta.startswith("ADJS"):
            rasgos = self._rasgos_en_subarbol(nodo, hojas_con_rasgos)
            dets = [r for r in rasgos if r.get("cat") == "Det"]
            ns = [r for r in rasgos if r.get("cat") == "N"]
            adjs = [r for r in rasgos if r.get("cat") == "Adj"]

            for d in dets:
                for n in ns:
                    if not self._compatibles(d.get("gen"), n.get("gen")):
                        errores.append(
                            f"Discordancia de género entre Det y N en '{nodo.etiqueta}'"
                        )
                    if not self._compatibles(d.get("num"), n.get("num")):
                        errores.append(
                            f"Discordancia de número entre Det y N en '{nodo.etiqueta}'"
                        )
                for adj in adjs:
                    if not self._compatibles(d.get("gen"), adj.get("gen")):
                        errores.append(
                            f"Discordancia de género entre Det y Adj en '{nodo.etiqueta}'"
                        )
                    if not self._compatibles(d.get("num"), adj.get("num")):
                        errores.append(
                            f"Discordancia de número entre Det y Adj en '{nodo.etiqueta}'"
                        )

            for n in ns:
                for adj in adjs:
                    if not self._compatibles(n.get("gen"), adj.get("gen")):
                        errores.append(
                            f"Discordancia de género entre N y Adj en '{nodo.etiqueta}'"
                        )
                    if not self._compatibles(n.get("num"), adj.get("num")):
                        errores.append(
                            f"Discordancia de número entre N y Adj en '{nodo.etiqueta}'"
                        )

        # 2. Concordancia sujeto - verbo en oraciones 'O' y 'Os'
        if nodo.etiqueta in ("O", "Os") and len(nodo.hijos) >= 2:
            sujeto_nodo, predicado_nodo = nodo.hijos[0], nodo.hijos[1]
            pers_suj, num_suj = self._extraer_pn_sujeto(sujeto_nodo, hojas_con_rasgos)
            verbos_directos = self._verbos_directos_sv(predicado_nodo, hojas_con_rasgos)

            for v in verbos_directos:
                if pers_suj is not None and v.get("pers") is not None and v.get("pers") != pers_suj:
                    errores.append(
                        f"Discordancia de persona: sujeto ({pers_suj}) vs verbo ({v.get('pers')})"
                    )
                if num_suj is not None and v.get("num") is not None and v.get("num") != num_suj:
                    errores.append(
                        f"Discordancia de número: sujeto ({num_suj}) vs verbo ({v.get('num')})"
                    )
                if nodo.etiqueta == "Os" and v.get("modo") != "subj":
                    errores.append(
                        f"Se esperaba modo subjuntivo en '{nodo.etiqueta}', se obtuvo '{v.get('modo')}'"
                    )

        for hijo in nodo.hijos:
            self._chequear_nodo(hijo, hojas_con_rasgos, errores)

    def _extraer_pn_sujeto(self, nodo_suj: Nodo, hojas_con_rasgos: list):
        rasgos = self._rasgos_en_subarbol(nodo_suj, hojas_con_rasgos)
        for r in rasgos:
            if r.get("cat") == "Pron":
                return r.get("pers"), r.get("num")
        for r in rasgos:
            if r.get("cat") in ("NP", "N"):
                return 3, r.get("num", "s")
        return None, None

    def _verbos_directos_sv(self, nodo_sv: Nodo, hojas_con_rasgos: list) -> list[dict]:
        # Evita descender a oraciones subordinadas ('O' o 'Os') dentro del SV
        if nodo_sv.etiqueta in ("O", "Os"):
            return []
        if not nodo_sv.hijos:
            return [r for r in self._rasgos_en_subarbol(nodo_sv, hojas_con_rasgos) if r.get("cat") == "V"]
        verbos = []
        for h in nodo_sv.hijos:
            if h.etiqueta not in ("O", "Os"):
                verbos.extend(self._verbos_directos_sv(h, hojas_con_rasgos))
        return verbos