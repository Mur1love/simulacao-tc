#!/usr/bin/env python3
"""
simular.py

Script principal que integra:
 - força bruta
 - ataque de dicionário
 - coleta de métricas

E permite escolher tudo via menu.
"""

import os
import time
from pathlib import Path

from ataque_dicionario import ataque_dicionario

# Importações dos scripts auxiliares
from automato_parser import carregar_automato
from brute_force import brute_force
from coleta_metricas import salvar_metricas
from simulador_afd import simular

# -----------------------------------------------------
# Configurações fixas
# -----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

AUTOMATOS_DIR = BASE_DIR / "automatos"
DICIONARIOS_DIR = BASE_DIR / "dicionarios"
RESULTADOS_DIR = BASE_DIR / "resultados"

RESULTADOS_DIR.mkdir(exist_ok=True)


# Abalfetos por política
ALFABETOS = {
    "fraca": "abcdefghijklmnopqrstuvwxyz0123456789",
    "media": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    "forte": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*-_=+/?",
}

TAMANHOS = {"fraca": (4, 6), "media": (6, 8), "forte": (8, 10)}


# -----------------------------------------------------
# Funções auxiliares
# -----------------------------------------------------


def selecionar_politica():
    print("\nEscolha o automato/política de senha:")
    print("1 - Fraca")
    print("2 - Média")
    print("3 - Forte")

    op = input("> ")

    if op == "1":
        return "fraca"
    if op == "2":
        return "media"
    if op == "3":
        return "forte"

    print("Opção inválida.")
    return selecionar_politica()


def selecionar_ataque():
    print("\nEscolha o tipo de ataque:")
    print("1 - Força bruta")
    print("2 - Dicionário")
    print("3 - Ambos")
    op = input("> ")

    if op in ["1", "2", "3"]:
        return op

    print("Opção inválida.")
    return selecionar_ataque()


# -----------------------------------------------------
# Execução principal
# -----------------------------------------------------


def main():
    print("\n===== SIMULAÇÃO DE ATAQUES A POLÍTICAS DE SENHA =====")

    politica = selecionar_politica()
    ataque_opcao = selecionar_ataque()

    jff_path = AUTOMATOS_DIR / f"{politica}.jff"

    print(f"\nSelecionado: {politica.upper()}")
    print("Carregando automato:", jff_path)

    # Coletor de métricas
    metricas = {
        "politica": politica,
        "tentativas": "-",
        "validas": "-",
        "tempo": "-",
        "aceitas_dic": "-",
        "taxa_dic": "-",
    }

    # -----------------------------
    # 1) ATAQUE DE FORÇA BRUTA
    # -----------------------------
    if ataque_opcao in ["1", "3"]:
        print("\n>>> Executando ataque de força bruta...")
        alfabeto = ALFABETOS[politica]
        min_len, max_len = TAMANHOS[politica]

        out_csv = RESULTADOS_DIR / f"bruteforce_{politica}.csv"

        tentativas, validas, tempo = brute_force(
            jff=jff_path,
            alfabeto=alfabeto,
            min_len=min_len,
            max_len=max_len,
            out_csv=out_csv,
        )

        metricas["tentativas"] = tentativas
        metricas["validas"] = validas
        metricas["tempo"] = f"{tempo:.2f}"

    # -----------------------------
    # 2) ATAQUE DE DICIONÁRIO
    # -----------------------------
    if ataque_opcao in ["2", "3"]:
        print("\n>>> Executando ataque de dicionário...")

        dict_path = DICIONARIOS_DIR / "top200-2025.txt"
        out_csv = RESULTADOS_DIR / f"dicionario_{politica}.csv"

        total, aceitas, taxa = ataque_dicionario(
            jff=jff_path, dict_path=dict_path, out_csv=out_csv
        )

        metricas["aceitas_dic"] = aceitas
        metricas["taxa_dic"] = f"{taxa:.4f}"

    # -----------------------------
    # 3) GERAR CSV FINAL
    # -----------------------------
    final_csv = RESULTADOS_DIR / "metricas_finais.csv"

    salvar_metricas(
        out_csv=final_csv,
        linhas=[
            [
                metricas["politica"],
                metricas["tentativas"],
                metricas["validas"],
                metricas["tempo"],
                metricas["aceitas_dic"],
                metricas["taxa_dic"],
            ]
        ],
    )

    print("\n===== SIMULAÇÃO FINALIZADA =====")
    print("Resultados salvos em:")
    print(" ->", final_csv)
    print(" -> Pasta completa:", RESULTADOS_DIR)


if __name__ == "__main__":
    main()
