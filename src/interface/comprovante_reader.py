"""
comprovante_reader.py - Leitura de notas fiscais e extração de dados via OCR (Tesseract)
"""

import os
import re
import cv2
import pytesseract
import numpy as np
from PIL import Image
from tkinter import filedialog, Tk
from core.utils import salvar_log

import shutil
import tempfile


# Configura o caminho do executável do Tesseract (ajustável por variável de ambiente)
pytesseract.pytesseract.tesseract_cmd = os.getenv(
    "TESSERACT_CMD",
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def selecionar_comprovante() -> str:
    """
    Abre um diálogo para o usuário selecionar uma imagem de nota fiscal.

    Returns:
        str: Caminho completo da imagem selecionada.
    """
    root = Tk()
    root.withdraw()  # Oculta a janela principal
    caminho = filedialog.askopenfilename(
        title="Selecione a imagem da nota fiscal",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.tiff *.bmp *.webp")]
    )
    root.destroy()
    return caminho

def copiar_para_temp(path_origem):
    temp_dir = tempfile.gettempdir()
    novo_caminho = os.path.join(temp_dir, "comprovante.jpg")
    shutil.copy(path_origem, novo_caminho)
    return novo_caminho

def aplicar_ocr_em_imagem(path_imagem: str) -> str:
    """
    Lê o texto de uma imagem utilizando OCR (Tesseract).

    Args:
        path_imagem (str): Caminho da imagem da nota fiscal.

    Returns:
        str: Texto bruto extraído da imagem.
    """
    # path = os.path.normpath(path_imagem)
    path_limpo = copiar_para_temp(path_imagem)
    imagem = cv2.imread(path_limpo)

    if imagem is None:
        raise FileNotFoundError("Imagem não encontrada ou não suportada.")

    # Pré-processamento
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    imagem_eq = cv2.equalizeHist(imagem_cinza)
    _, binarizada = cv2.threshold(imagem_eq, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    texto = pytesseract.image_to_string(binarizada, lang="por")
    return texto


import re

def extrair_campos_nota(texto: str) -> dict:
    """
    Extrai campos relevantes de uma nota fiscal a partir do texto OCR usando expressões regulares.

    Args:
        texto (str): Texto bruto retornado pelo OCR.

    Returns:
        dict: Dicionário com os campos extraídos.
    """
    campos = {}

    # Chave de acesso
    chave = re.search(r'(\d{44}|\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{2})', texto)
    if chave:
        campos["Chave de Acesso"] = chave.group().replace(" ", "")

    # CNPJ emissor
    cnpj = re.search(r'CNPJ\s*[:\-]?\s*(\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})', texto, re.IGNORECASE)
    if cnpj:
        campos["CNPJ"] = cnpj.group(1)

    # Data de emissão
    data_emissao = re.search(r'(\d{2}/\d{2}/\d{4})', texto)
    if data_emissao:
        campos["Data de Emissão"] = data_emissao.group(1)

    # Valor total
    valor_total = re.search(r'(Valor\s+Total|Total\s+da\s+Nota)\s*[:\-]?\s*R?\$?\s*([\d.,]+)', texto, re.IGNORECASE)
    if valor_total:
        campos["Valor Total"] = valor_total.group(2)

    # Itens detalhados
    itens = re.findall(
        r'(?P<codigo>\d{5,})\s+(?P<nome>.+?)\s+(?P<quant>\d+[,.]?\d*)\s+\w+\s+x\s+(?P<unitario>\d+[,.]?\d*)\s*=\s*(?P<total>\d+[,.]?\d*)',
        texto
    )

        # Itens da nota (linha por linha com quantidade, unitário, total)
    linhas_item = re.findall(
        r'(\d+)\s+(\d{8,13})\s+(.+?)\s+(\d+[.,]?\d*)\s+\w+\s+x\s+([\d.,]+)\s+([\d.,]+)',
        texto,
        re.IGNORECASE
    )

    if linhas_item:
        campos["Itens"] = []
        for i, item in enumerate(linhas_item, 1):
            campos["Itens"].append({
                "Item Nº": i,
                "Código": item[1],
                "Nome": item[2].strip(),
                "Quantidade": item[3],
                "Valor Unitário": item[4],
                "Valor Total Item": item[5]
            })


    return campos

def usar_comprovante():
    """
    Seleciona uma imagem de nota fiscal, aplica OCR e extrai os campos relevantes via regex.
    """
    caminho = selecionar_comprovante()
    if not caminho:
        print("Nenhum arquivo selecionado.")
        return

    try:
        print("🧠 Extraindo texto com OCR...")
        texto_extraido = aplicar_ocr_em_imagem(caminho)

        campos = extrair_campos_nota(texto_extraido)

        if campos:
            print("\n📋 Campos extraídos:")
            for k, v in campos.items():
                print(f"{k}: {v}")
            salvar_log(list(campos.items()))
        else:
            print("⚠️ Nenhum campo estruturado foi detectado.")
            salvar_log([("Texto OCR", texto_extraido)])

    except Exception as e:
        print(f"Erro ao processar o comprovante: {e}")
