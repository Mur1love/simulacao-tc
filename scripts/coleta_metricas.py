import os

import pandas as pd


def export_metrics_to_csv(data, filename, output_dir="simulacao-tc/resultados"):
    """
    Exporta os dados das métricas para um arquivo CSV.

    Args:
        data (dict): Dicionário contendo os dados a serem exportados.
                     As chaves serão os nomes das colunas.
        filename (str): Nome do arquivo CSV (ex: "dicionario.csv").
        output_dir (str): Diretório onde o arquivo CSV será salvo.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, filename)
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    print(f"Métricas exportadas para: {filepath}")


if __name__ == "__main__":
    # Exemplo de uso para teste
    sample_data_brute_force = {
        "politica": ["Fraca", "Media", "Forte"],
        "tempo_total_segundos": [10.5, 60.2, 120.1],
        "senhas_testadas": [10000, 50000, 100000],
        "senhas_aceitas": [8000, 40000, 70000],
    }
    export_metrics_to_csv(sample_data_brute_force, "brute_force.csv")

    sample_data_dicionario = {
        "politica": ["Fraca", "Media", "Forte"],
        "dicionario": ["10k", "10k", "10k"],
        "senhas_testadas": [10000, 10000, 10000],
        "senhas_aceitas": [500, 100, 10],
        "taxa_sucesso": [0.05, 0.01, 0.001],
    }
    export_metrics_to_csv(sample_data_dicionario, "dicionario.csv")
