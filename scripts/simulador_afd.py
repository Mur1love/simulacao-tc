#!/usr/bin/env python3
"""
simulador_afd.py
Simula um autômato finito determinístico carregado pelo automato_parser.py
"""


def simular(automato, palavra):
    estado_atual = automato.inicial

    for simbolo in palavra:
        trans = automato.transicoes.get(estado_atual, {})
        if simbolo not in trans:
            return False
        estado_atual = trans[simbolo]

    return estado_atual in automato.finais
