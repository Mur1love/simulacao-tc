#!/usr/bin/env python3
"""
brute_force.py
Gera todo o espaço de senhas possíveis e testa no AFD.
"""

import csv
import itertools
import time
from pathlib import Path

from automato_parser import carregar_automato
from simulador_afd import simular


def brute_force(jff, alfabeto, min_len, max_len, out_csv):
    automato = carregar_automato(jff)

    tentativas = 0
    validas = 0
    inicio = time.time()

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["senha", "aceita"])

        for tam in range(min_len, max_len + 1):
            for comb in itertools.product(alfabeto, repeat=tam):
                senha = "".join(comb)
                tentativas += 1
                ok = simular(automato, senha)
                if ok:
                    validas += 1
                w.writerow([senha, int(ok)])

    tempo = time.time() - inicio
    print("FORÇA BRUTA FINALIZADA")
    print(f"Tentativas: {tentativas}")
    print(f"Senhas válidas: {validas}")
    print(f"Tempo total: {tempo:.2f}s")

    return tentativas, validas, tempo
