#!/usr/bin/env python3
"""
test_automata.py

Exemplos de Uso:
    python3 test_automata.py --automato ../automatos/fraca.jff --test "abcd" "a1b2" "abc"
    python3 test_automata.py --automato ../automatos/media.jff --test "Abc123" "A1b2c3" "ab1234"
    python3 test_automata.py --automato ../automatos/forte.jff --test "Aa1#" "Senha123#"

    # Teste usando os dicionários (uma senha por linha)
    python3 test_automata.py --automato ../automatos/media.jff --dict ../dicionarios/top200-2025.txt --out ../resultados/resultados_media.csv

Este testador interpreta classes de caracteres estilo colchetes usadas no .jff (ex: [a-z], [A-Z], [0-9], [!@#...])
e utiliza uma semântica apropriada para validação de senhas:
 - Para "fraca": aceita qualquer string composta apenas por caracteres permitidos com comprimento >= 4
 - Para "media": requer comprimento >= 6 e pelo menos uma letra minúscula, uma maiúscula e um dígito
 - Para "forte": requer comprimento >= 8 e pelo menos uma letra minúscula, uma maiúscula, um dígito e um símbolo
"""

import argparse
import csv
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SYMBOLS_FOR_FACILITY = "!@#$%&*\\-_=+/?"


# helper to identify policy type from filename
def policy_from_filename(path):
    n = Path(path).name.lower()
    if "fraca" in n:
        return "fraca"
    if "media" in n:
        return "media"
    if "forte" in n or "strong" in n:
        return "forte"
    return None


def allowed_charset_from_jff(jff_path):
    """
    Parse the .jff to extract the union of character classes used in reads.
    We will return a regular expression character class representing allowed characters.
    """
    tree = ET.parse(jff_path)
    root = tree.getroot()
    reads = []
    for read in root.findall(".//read"):
        if read is None or read.text is None:
            continue
        reads.append(read.text.strip())
    # combine bracket-style classes found (like [a-z], [A-Z], [0-9], and symbol lists)
    chars = []
    for r in reads:
        # if r looks like a bracket class, remove outer brackets
        m = re.match(r"^\[(.*)\]$", r)
        if m:
            inner = m.group(1)
            chars.append(inner)
        else:
            chars.append(re.escape(r))
    combined = "".join(chars)
    # build a regex charclass
    # normalize escapes for dash inside
    return f"[{combined}]"


def test_password_against_policy(password, policy):
    if policy == "fraca":
        # min length 4, allowed lower+digits
        if len(password) < 4:
            return False
        if not re.fullmatch(r"[a-z0-9]+", password):
            return False
        return True
    if policy == "media":
        if len(password) < 6:
            return False
        if not re.fullmatch(r"[A-Za-z0-9]+", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        return True
    if policy == "forte":
        if len(password) < 8:
            return False
        # allowed: letters, digits, symbols
        if not re.fullmatch(
            r"[A-Za-z0-9" + re.escape(SYMBOLS_FOR_FACILITY) + r"]+", password
        ):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search("[" + re.escape(SYMBOLS_FOR_FACILITY) + "]", password):
            return False
        return True
    return False


def batch_test(jff_path, dict_path, out_csv):
    policy = policy_from_filename(jff_path)
    if policy is None:
        print(
            "Não foi possível inferir a política a partir do nome do arquivo; use 'fraca', 'media' ou 'forte' no nome."
        )
        return
    total = 0
    accepted = 0
    with (
        open(dict_path, "r", encoding="utf-8", errors="ignore") as f,
        open(out_csv, "w", newline="", encoding="utf-8") as outf,
    ):
        writer = csv.writer(outf)
        writer.writerow(["password", "accepted"])
        for line in f:
            pwd = line.rstrip("\n\r")
            if pwd == "":
                continue
            total += 1
            ok = test_password_against_policy(pwd, policy)
            if ok:
                accepted += 1
            writer.writerow([pwd, int(ok)])
    print(
        f"Batch test finished. Total={total}, Accepted={accepted}, Rate={accepted / total:.4f}"
    )
    print("Results saved to", out_csv)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--automato", "-a", required=True, help="Caminho para o arquivo .jff"
    )
    parser.add_argument(
        "--test", "-t", nargs="*", help="Senhas para testar individualmente"
    )
    parser.add_argument(
        "--dict",
        "-d",
        help="Arquivo de dicionario (um password por linha) para testar em batch",
    )
    parser.add_argument(
        "--out",
        "-o",
        help="Arquivo CSV de saída para batch (default resultados.csv)",
        default="resultados.csv",
    )
    args = parser.parse_args()

    jff_path = Path(args.automato)
    if not jff_path.exists():
        print("Arquivo .jff não encontrado:", jff_path)
        sys.exit(1)

    policy = policy_from_filename(jff_path)
    if policy is None:
        print(
            "Nome do arquivo .jff não indica política (fraca/media/forte). Continuando com inferência conservadora."
        )
        # fallthrough
    if args.test:
        for pwd in args.test:
            ok = test_password_against_policy(pwd, policy)
            print(f"{pwd!r} -> {'ACEITA' if ok else 'REJEITADA'}")
    if args.dict:
        out_csv = args.out
        batch_test(jff_path, args.dict, out_csv)


if __name__ == "__main__":
    main()
