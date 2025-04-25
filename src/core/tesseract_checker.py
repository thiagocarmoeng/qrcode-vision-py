"""
tesseract_checker.py - Verifica se o Tesseract está instalado e o idioma 'por' está disponível.
"""

import os
import pytesseract
import subprocess


def verificar_tesseract_instalado() -> bool:
    """
    Verifica se o executável do Tesseract está acessível.

    Returns:
        bool: True se o Tesseract for encontrado, False caso contrário.
    """
    try:
        versao = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract instalado - versão: {versao}")
        return True
    except (EnvironmentError, pytesseract.pytesseract.TesseractNotFoundError) as e:
        print("❌ Tesseract não encontrado. Verifique se está instalado e se o caminho está correto.")
        print(f"Detalhes: {e}")
        return False


def verificar_idioma_portugues_instalado() -> bool:
    """
    Verifica se o idioma 'por' está disponível para o Tesseract.

    Returns:
        bool: True se o idioma estiver instalado, False caso contrário.
    """
    try:
        resultado = subprocess.run(
            [pytesseract.pytesseract.tesseract_cmd, '--list-langs'],
            capture_output=True,
            text=True
        )
        idiomas = resultado.stdout
        if 'por' in idiomas:
            print("✅ Idioma 'por' (Português) está instalado.")
            return True
        else:
            print("❌ Idioma 'por' (Português) NÃO está instalado.")
            return False
    except Exception as e:
        print(f"❌ Falha ao verificar idiomas disponíveis: {e}")
        return False


def executar_verificacao_completa():
    """
    Executa ambas verificações e orienta o usuário.
    """
    print("🔍 Verificando Tesseract OCR...")
    tesseract_ok = verificar_tesseract_instalado()
    
    if tesseract_ok:
        print("🔍 Verificando idioma 'por'...")
        verificar_idioma_portugues_instalado()


if __name__ == "__main__":
    executar_verificacao_completa()
