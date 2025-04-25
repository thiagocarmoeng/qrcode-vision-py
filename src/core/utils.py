"""
utils.py - Funções auxiliares para suporte ao sistema
"""

import os
import datetime
from typing import List, Tuple


def salvar_log(dados_detectados: List[Tuple[str, str]], pasta_log: str = "logs") -> None:
    """
    Salva os dados detectados e traduzidos em um arquivo de log .txt.

    Args:
        dados_detectados (List[Tuple[str, str]]): Lista de tuplas com (original, tradução)
        pasta_log (str): Nome da pasta onde os logs serão armazenados (padrão: 'logs')

    A função cria um arquivo com timestamp e armazena os dados de forma estruturada.
    """
    if not dados_detectados:
        return

    os.makedirs(pasta_log, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{pasta_log}/deteccao_qrcode_{timestamp}.txt"

    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        for original, traducao in dados_detectados:
            arquivo.write(f"Original: {original}\n")
            arquivo.write(f"Tradução: {traducao}\n")
            arquivo.write("=" * 50 + "\n")

    print(f"\nResultados salvos em: {nome_arquivo}")
