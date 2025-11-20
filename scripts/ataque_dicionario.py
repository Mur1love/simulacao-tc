#!/usr/bin/env python3
"""
ataque_dicionario.py
Testa listas de senhas contra o AFD gerado no JFLAP.
"""

import csv

from automato_parser import carregar_automato
from simulador_afd import simular


def ataque_dicionario(jff, dict_path, out_csv):
    automato = carregar_automato(jff)

    total = 0
    aceitas = 0

    with (
        open(dict_path, "r", encoding="utf-8", errors="ignore") as f,
        open(out_csv, "w", newline="", encoding="utf-8") as of,
    ):
        w = csv.writer(of)
        w.writerow(["password", "accepted"])

        for line in f:
            senha = line.strip()
            if senha == "":
                continue

            total += 1
            ok = simular(automato, senha)
            if ok:
                aceitas += 1

            w.writerow([senha, int(ok)])

    taxa = aceitas / total if total > 0 else 0
    print(f"Ataque de dicionário finalizado.")
    print(f"Total testadas: {total}")
    print(f"Aceitas: {aceitas}")
    print(f"Taxa: {taxa:.4f}")

    return total, aceitas, taxa
