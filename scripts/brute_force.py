import itertools
import math
import os
import time

import pandas as pd
from automato_parser import Automaton, parse_jff


def generate_brute_force_passwords(charset, max_length):
    """
    Gera senhas para ataque de força bruta.
    """
    password_index = 0
    for length in range(1, max_length + 1):
        for password_tuple in itertools.product(charset, repeat=length):
            password_index += 1
            yield "".join(password_tuple), password_index


def run_brute_force_attack_target(
    automaton_file,
    charset,
    min_length,
    max_length,
    target_password,
    time_limit_seconds=None,
):
    """
    Executa a simulação de ataque de força bruta para encontrar uma senha alvo
    e coleta métricas detalhadas.
    """
    automaton = parse_jff(automaton_file)
    total_passwords_tested = 0
    start_time = time.time()
    password_found_index = -1
    duration_until_found = -1
    attack_stopped_due_to_time_limit = False

    # Viabilidade computacional inicial (baseada no espaço de busca)
    alphabet_size = len(charset)
    total_search_space = 0
    for length in range(min_length, max_length + 1):
        total_search_space += alphabet_size**length

    viability_comment = "Viável para teste"
    if total_search_space > 10**8:  # Aprox. 100 milhões de senhas
        viability_comment = "Parcialmente viável (demorado)"
    if total_search_space > 10**12:  # Aprox. 1 trilhão de senhas
        viability_comment = "Inviável computacionalmente em tempo razoável"

    print(
        f"Iniciando ataque de força bruta para o autômato {os.path.basename(automaton_file)} "
        f"com senha alvo '{target_password}'..."
    )
    print(
        f"Charset: '{''.join(charset)}', Comprimento Min: {min_length}, Comprimento Max: {max_length}"
    )

    for password, index in generate_brute_force_passwords(charset, max_length):
        current_time = time.time()
        duration_so_far = current_time - start_time
        if time_limit_seconds is not None and duration_so_far > time_limit_seconds:
            print(
                f"Limite de tempo ({time_limit_seconds}s) atingido para o autômato "
                f"{os.path.basename(automaton_file)} e senha alvo '{target_password}'."
            )
            attack_stopped_due_to_time_limit = True
            total_passwords_tested = index  # Record passwords tested up to this point
            break  # Stop the brute-force attempt

        if len(password) < min_length:
            continue

        total_passwords_tested = index
        if automaton.accepts(password):
            if password == target_password:
                end_time = time.time()
                duration_until_found = end_time - start_time
                password_found_index = index
                print(f"Senha alvo '{target_password}' encontrada!")
                break

    # After the loop, calculate final duration and process results
    final_duration_of_attempt = time.time() - start_time

    estimated_time_to_crack_total_seconds = "N/A"
    velocity_attempts_per_second = "N/A"
    final_viability_comment = viability_comment
    is_viable_result = "Não"  # Default to No, update to Yes if found and within original viability bounds

    if password_found_index != -1:  # Password was found
        velocity_attempts_per_second = (
            total_passwords_tested / duration_until_found
            if duration_until_found > 0
            else 0
        )
        is_viable_result = "Sim"
        # If password found, the original viability_comment based on total search space is still relevant.
    else:  # Password not found (either exhausted space or hit time limit)
        # Calculate velocity based on actual run time
        if final_duration_of_attempt > 0 and total_passwords_tested > 0:
            velocity_attempts_per_second = (
                total_passwords_tested / final_duration_of_attempt
            )
            # Estimate time to crack the *full* search space if it wasn't exhausted
            if (
                total_passwords_tested < total_search_space
                and velocity_attempts_per_second > 0
            ):
                estimated_time_to_crack_total_seconds = (
                    total_search_space / velocity_attempts_per_second
                )
                # Justify inviability with estimation
                final_viability_comment = (
                    f"Inviável (senha não encontrada no limite de tempo ou espaço de busca exaurido). "
                    f"Estimativa de tempo para quebra: {estimated_time_to_crack_total_seconds / 3600:.2f} horas "
                    f"({estimated_time_to_crack_total_seconds / (3600 * 24):.2f} dias). (Velocidade de {velocity_attempts_per_second:.2f} senhas/s)"
                )
            else:  # Exhausted space, but password not found, or velocity zero
                final_viability_comment = "Inviável (senha não encontrada após exaurir espaço ou limite de tempo)."
        else:  # No passwords tested or zero duration, cannot estimate
            final_viability_comment = "Inviável (senha não encontrada)."

        is_viable_result = "Não"  # Explicitly not viable if not found

    results = {
        "automaton": os.path.basename(automaton_file),
        "target_password": target_password,
        "charset": "".join(charset),
        "min_length": min_length,
        "max_length": max_length,
        "attempts_until_crack": total_passwords_tested
        if password_found_index != -1
        else (
            f"{total_passwords_tested} (limite de tempo atingido)"
            if attack_stopped_due_to_time_limit
            else "Não encontrada (espaço exaurido)"
        ),
        "time_until_crack_seconds": f"{duration_until_found:.4f}"
        if password_found_index != -1
        else f"{final_duration_of_attempt:.4f} (até o limite ou fim da busca)",
        "velocity_attempts_per_second": f"{velocity_attempts_per_second:.2f}"
        if isinstance(velocity_attempts_per_second, (int, float))
        and velocity_attempts_per_second > 0
        else "N/A",
        "alphabet_size": alphabet_size,
        "password_index_in_space": password_found_index
        if password_found_index != -1
        else (
            f"{total_passwords_tested} (limite de tempo atingido)"
            if attack_stopped_due_to_time_limit
            else "Não encontrada (espaço exaurido)"
        ),
        "total_search_space": total_search_space,
        "estimated_time_to_crack_total_seconds": (
            f"{estimated_time_to_crack_total_seconds:.2f}"
            if isinstance(estimated_time_to_crack_total_seconds, (int, float))
            else estimated_time_to_crack_total_seconds
        ),
        "viability_comment": final_viability_comment,
        "is_viable": is_viable_result,
    }

    return results


if __name__ == "__main__":
    AUTOMATA_DIR = "../automatos"
    OUTPUT_DIR = "../resultados"  # Alterado para "../resultados"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Caracteres comuns para políticas de senha (minúsculas, maiúsculas, dígitos, símbolos)
    charset_fraca = "abcdefghijklmnopqrstuvwxyz0123456789"
    charset_media = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    charset_forte = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?`~"

    time_limit_per_test_seconds = 60  # 1 minute limit for each test

    # Política Fraca: min 4, sem requisitos de caracteres, apenas minúsculas e dígitos
    # Senha alvo "abcd" - deve ser facilmente encontrada
    target_fraca = "ac12"
    results_fraca = run_brute_force_attack_target(
        os.path.join(AUTOMATA_DIR, "fraca.jff"),
        charset_fraca,
        min_length=4,
        max_length=4,
        target_password=target_fraca,
        time_limit_seconds=time_limit_per_test_seconds,
    )
    df_fraca = pd.DataFrame([results_fraca])
    output_path_fraca = os.path.join(
        OUTPUT_DIR,
        f"brute_force_target_fraca_{target_fraca}.csv",
    )
    df_fraca.to_csv(output_path_fraca, index=False)
    print(f"Resultados para a política Fraca salvos em {output_path_fraca}\n")

    # Política Média: min 6, 1 minúscula, 1 maiúscula, 1 dígito
    # Senha alvo "aA1aaa" - deve ser encontrada em um espaço de busca maior
    target_media = "aA1aaa"
    results_media = run_brute_force_attack_target(
        os.path.join(AUTOMATA_DIR, "media.jff"),
        charset_media,
        min_length=6,
        max_length=6,
        target_password=target_media,
        time_limit_seconds=time_limit_per_test_seconds,
    )
    df_media = pd.DataFrame([results_media])
    output_path_media = os.path.join(
        OUTPUT_DIR,
        f"brute_force_target_media_{target_media}.csv",
    )
    df_media.to_csv(output_path_media, index=False)
    print(f"Resultados para a política Média salvos em {output_path_media}\n")

    # Política Forte: min 8, 1 minúscula, 1 maiúscula, 1 dígito, 1 especial
    # Senha alvo "aA1!bbcc" - ainda maior espaço de busca
    target_forte = "aA1!bbcc"
    results_forte = run_brute_force_attack_target(
        os.path.join(AUTOMATA_DIR, "forte.jff"),
        charset_forte,
        min_length=8,
        max_length=8,
        target_password=target_forte,
        time_limit_seconds=time_limit_per_test_seconds,
    )
    df_forte = pd.DataFrame([results_forte])
    output_path_forte = os.path.join(
        OUTPUT_DIR,
        f"brute_force_target_forte_{target_forte}.csv",
    )
    df_forte.to_csv(output_path_forte, index=False)
    print(f"Resultados para a política Forte salvos em {output_path_forte}\n")
