#!/usr/bin/env python3
"""
coleta_metricas.py
Organiza métricas das simulações em um único CSV final.
"""

import csv


def salvar_metricas(out_csv, linhas):
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            ["politica", "tentativas", "validas", "tempo", "aceitas_dic", "taxa_dic"]
        )
        for linha in linhas:
            w.writerow(linha)

    print("Métricas salvas em", out_csv)
