#!/usr/bin/env python3
"""Cuenta días de presencia por país a partir de un registro de viajes.

Entrada: CSV con columnas pais,entrada,salida (fechas AAAA-MM-DD).
- `salida` vacía = sigue en el país (se cuenta hasta hoy o hasta --hasta).
- Se cuentan como día de presencia tanto el día de entrada como el de salida
  (criterio conservador: un día de viaje cuenta en ambos países). Usa
  --sin-dia-salida para no contar el día de salida.

Salida:
- Días por país y año natural (criterio español, art. 9 LIRPF: >183 días).
- Para Colombia (o el país indicado con --pais-ventana): máximo de días en
  cualquier ventana móvil de 365 días que termine en cada año, y la primera
  fecha en que se superan 183 días (criterio art. 10 E.T. colombiano).

Uso:
    python contar_dias.py viajes.csv [--hasta AAAA-MM-DD] [--pais-ventana CO] [--json]
"""
import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import date, timedelta


def parse_date(s):
    return date.fromisoformat(s.strip())


def load(path, hasta, sin_dia_salida):
    dias = defaultdict(set)  # pais -> set(date)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = {"pais", "entrada", "salida"} - set(reader.fieldnames or [])
        if missing:
            sys.exit(f"Faltan columnas en el CSV: {', '.join(sorted(missing))}")
        for n, row in enumerate(reader, start=2):
            pais = row["pais"].strip().upper()
            if not pais:
                continue
            try:
                ini = parse_date(row["entrada"])
                fin = parse_date(row["salida"]) if row["salida"].strip() else hasta
            except ValueError as e:
                sys.exit(f"Fecha inválida en la línea {n}: {e}")
            if sin_dia_salida and row["salida"].strip():
                fin -= timedelta(days=1)
            fin = min(fin, hasta)
            if fin < ini:
                continue
            d = ini
            while d <= fin:
                dias[pais].add(d)
                d += timedelta(days=1)
    return dias


def por_anio(dias):
    out = defaultdict(lambda: defaultdict(int))
    for pais, ds in dias.items():
        for d in ds:
            out[d.year][pais] += 1
    return out


def ventana_365(ds):
    """Devuelve (max_por_anio, primera_fecha_>183)."""
    if not ds:
        return {}, None
    orden = sorted(ds)
    inicio, fin = orden[0], orden[-1]
    presentes = set(ds)
    count = 0
    max_por_anio = defaultdict(int)
    primera = None
    d = inicio
    while d <= fin:
        if d in presentes:
            count += 1
        salida = d - timedelta(days=365)
        if salida in presentes:
            count -= 1
        max_por_anio[d.year] = max(max_por_anio[d.year], count)
        if primera is None and count > 183:
            primera = d
        d += timedelta(days=1)
    return dict(max_por_anio), primera


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--hasta", default=date.today().isoformat())
    ap.add_argument("--pais-ventana", default="CO")
    ap.add_argument("--sin-dia-salida", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    hasta = parse_date(a.hasta)
    dias = load(a.csv, hasta, a.sin_dia_salida)
    anios = por_anio(dias)
    pv = a.pais_ventana.upper()
    max_v, primera = ventana_365(dias.get(pv, set()))

    solapes = set()
    paises = list(dias)
    for i, p in enumerate(paises):
        for q in paises[i + 1:]:
            solapes |= dias[p] & dias[q]

    if a.json:
        print(json.dumps({
            "hasta": hasta.isoformat(),
            "por_anio": {y: dict(v) for y, v in sorted(anios.items())},
            "ventana_365": {"pais": pv, "max_por_anio": max_v,
                            "primera_fecha_mas_de_183": primera.isoformat() if primera else None},
            "dias_en_dos_paises": len(solapes),
        }, indent=2, ensure_ascii=False))
        return

    print(f"Registro contado hasta {hasta.isoformat()}\n")
    print("Días por año natural (criterio España: >183 en el año):")
    for y in sorted(anios):
        partes = ", ".join(f"{p}: {n}" for p, n in sorted(anios[y].items()))
        marca = " ⚠ ES >183" if anios[y].get("ES", 0) > 183 else ""
        print(f"  {y}: {partes}{marca}")
    print(f"\nMáximo de días en {pv} en cualquier ventana de 365 días (criterio Colombia: >183):")
    for y in sorted(max_v):
        marca = " ⚠ >183" if max_v[y] > 183 else ""
        print(f"  ventana que termina en {y}: {max_v[y]}{marca}")
    print(f"  Primera fecha en que se superan 183 días: {primera.isoformat() if primera else 'no se superan'}")
    if solapes:
        print(f"\nAviso: {len(solapes)} día(s) cuentan en dos países (días de viaje).")


if __name__ == "__main__":
    main()
