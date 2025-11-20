#!/usr/bin/env python3
"""
automato_parser.py
Lê um arquivo .jff e converte para uma estrutura de AFD utilizável pelo Python.
"""

import xml.etree.ElementTree as ET


class Automato:
    def __init__(self, estados, inicial, finais, transicoes):
        self.estados = estados
        self.inicial = inicial
        self.finais = finais
        self.transicoes = transicoes  # dict[state][symbol] = next_state


def carregar_automato(jff_path):
    tree = ET.parse(jff_path)
    root = tree.getroot()

    estados = {}
    inic = None
    finais = set()
    trans = {}

    for state in root.findall(".//state"):
        sid = state.get("id")
        name = state.get("name")
        estados[sid] = name

        if state.find("initial") is not None:
            inic = sid

        if state.find("final") is not None:
            finais.add(sid)

        trans[sid] = {}

    for t in root.findall(".//transition"):
        from_element = t.find("from")
        de = from_element.text if from_element is not None else ""

        to_element = t.find("to")
        para = to_element.text if to_element is not None else ""

        read_element = t.find("read")
        leitura = read_element.text if read_element is not None else ""

        trans[de].setdefault(leitura, para)

    return Automato(estados, inic, finais, trans)
