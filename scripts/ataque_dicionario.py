import os
import time

import pandas as pd
from automato_parser import Automaton, parse_jff


class AtaqueDicionario:
    def __init__(self, resultados_dir="resultados"):
        self.resultados_dir = resultados_dir
        os.makedirs(self.resultados_dir, exist_ok=True)

    def executar_ataque(self, nome_politica, dicionario_path, automato_path):
        print(
            f"Iniciando ataque de dicionário para a política '{nome_politica}' com o dicionário '{dicionario_path}'..."
        )

        automato = parse_jff(automato_path)

        if automato is None:
            print(
                f"Erro ao carregar o autômato para '{nome_politica}'. Pulando este ataque."
            )
            return

        senhas_testadas = []
        senhas_aceitas = []

        start_time = time.time()

        with open(dicionario_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                senha = line.strip()
                senhas_testadas.append(senha)
                if automato.accepts(senha):
                    senhas_aceitas.append(senha)

        end_time = time.time()
        tempo_total = end_time - start_time

        total_senhas_testadas = len(senhas_testadas)
        total_senhas_aceitas = len(senhas_aceitas)
        taxa_sucesso = (
            (total_senhas_aceitas / total_senhas_testadas) * 100
            if total_senhas_testadas > 0
            else 0
        )

        print(f"Ataque para '{nome_politica}' concluído.")
        print(f"Total de senhas testadas: {total_senhas_testadas}")
        print(f"Total de senhas aceitas: {total_senhas_aceitas}")
        print(f"Taxa de sucesso: {taxa_sucesso:.2f}%")
        print(f"Tempo total: {tempo_total:.2f} segundos")

        resultados = {
            "politica": nome_politica,
            "dicionario": os.path.basename(dicionario_path),
            "total_senhas_testadas": total_senhas_testadas,
            "total_senhas_aceitas": total_senhas_aceitas,
            "taxa_sucesso": taxa_sucesso,
            "tempo_total_segundos": tempo_total,
        }

        return resultados

    def salvar_resultados_csv(self, todos_resultados, filename="dicionario.csv"):
        df = pd.DataFrame(todos_resultados)
        filepath = os.path.join(self.resultados_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"Resultados do ataque de dicionário salvos em: {filepath}")


if __name__ == "__main__":
    # Exemplo de uso (requer automato_parser.py e a classe Automato)
    # Por enquanto, vamos criar um mock para o AutomatoParser e Automato

    # Dicionários de exemplo (ajuste os caminhos conforme sua estrutura)
    dicionarios_dir = "dicionarios"
    automatos_dir = "automatos"

    dict_10k_path = os.path.join(dicionarios_dir, "10k.txt")
    dict_top200_path = os.path.join(dicionarios_dir, "top200-2025.txt")

    # Autômatos de exemplo
    automato_fraca_path = os.path.join(automatos_dir, "fraca.jff")
    automato_media_path = os.path.join(automatos_dir, "media.jff")
    automato_forte_path = os.path.join(automatos_dir, "forte.jff")

    # Instancia o atacante
    atacante = AtaqueDicionario()

    todos_resultados = []

    todos_resultados = []

    # Combinações para Política Fraca
    resultados_fraca_10k = atacante.executar_ataque(
        "fraca", dict_10k_path, automato_fraca_path
    )
    if resultados_fraca_10k:
        todos_resultados.append(resultados_fraca_10k)

    resultados_fraca_top200 = atacante.executar_ataque(
        "fraca", dict_top200_path, automato_fraca_path
    )
    if resultados_fraca_top200:
        todos_resultados.append(resultados_fraca_top200)

    # Combinações para Política Média
    resultados_media_10k = atacante.executar_ataque(
        "media", dict_10k_path, automato_media_path
    )
    if resultados_media_10k:
        todos_resultados.append(resultados_media_10k)

    resultados_media_top200 = atacante.executar_ataque(
        "media", dict_top200_path, automato_media_path
    )
    if resultados_media_top200:
        todos_resultados.append(resultados_media_top200)

    # Combinações para Política Forte
    resultados_forte_10k = atacante.executar_ataque(
        "forte", dict_10k_path, automato_forte_path
    )
    if resultados_forte_10k:
        todos_resultados.append(resultados_forte_10k)

    resultados_forte_top200 = atacante.executar_ataque(
        "forte", dict_top200_path, automato_forte_path
    )
    if resultados_forte_top200:
        todos_resultados.append(resultados_forte_top200)

    # Salva todos os resultados em um único CSV
    if todos_resultados:
        atacante.salvar_resultados_csv(todos_resultados)

    print("\nSimulação de ataque de dicionário concluída.")
    print("Simulação concluída com o automato_parser.py real.")
