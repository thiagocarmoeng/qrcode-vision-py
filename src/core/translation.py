"""
translation.py - Módulo de tradução automática com uso de cache
"""

from googletrans import Translator

# Cache global para armazenar traduções já feitas
cache_traducoes = {}


def traduzir_texto(texto: str, idioma_destino: str = 'pt') -> str:
    """
    Traduz um texto para o idioma especificado.

    Args:
        texto (str): Texto de entrada (normalmente extraído de um QR Code).
        idioma_destino (str): Código do idioma de destino (padrão: 'pt').

    Returns:
        str: Texto traduzido
    """
    tradutor = Translator()
    resultado = tradutor.translate(texto, dest=idioma_destino)
    return resultado.text


def traduzir_texto_async(texto: str) -> None:
    """
    Tradução assíncrona que salva o resultado no cache global.

    Args:
        texto (str): Texto a ser traduzido

    Observação:
        Utilizado para tradução em segundo plano com threads, 
        evitando travamentos na leitura da câmera ou fluxo de captura.
    """
    try:
        traducao = traduzir_texto(texto)
        cache_traducoes[texto] = traducao
        print(f"Tradução concluída: {traducao}")
    except Exception as e:
        print(f"Erro na tradução de '{texto}': {e}")
        cache_traducoes[texto] = "Erro"
