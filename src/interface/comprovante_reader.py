import cv2
import numpy as np
import pytesseract
import re
import os
from tkinter import filedialog, Tk


# Configura o caminho do Tesseract (ajuste se necessário)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def selecionar_imagem() -> str:
    """Permite ao usuário escolher a imagem do comprovante."""
    root = Tk()
    root.withdraw()
    caminho = filedialog.askopenfilename(
        title="Selecione o comprovante",
        filetypes=[("Imagens", "*.jpg *.jpeg *.png")]
    )
    return caminho


def preprocessar_imagem(path_imagem: str) -> np.ndarray:
    """
    Faz o carregamento seguro e pré-processamento da imagem para OCR.
    """
    try:
        path_imagem = os.path.normpath(path_imagem)
        imagem_array = np.fromfile(path_imagem, dtype=np.uint8)
        imagem = cv2.imdecode(imagem_array, cv2.IMREAD_COLOR)

        if imagem is None:
            raise ValueError("Imagem não pôde ser carregada.")

        # Conversão para cinza
        cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        # Aumentar escala da imagem para melhorar OCR
        escala = 1.5
        largura = int(cinza.shape[1] * escala)
        altura = int(cinza.shape[0] * escala)
        redimensionada = cv2.resize(cinza, (largura, altura), interpolation=cv2.INTER_LINEAR)

        # Equalização do histograma
        equalizada = cv2.equalizeHist(redimensionada)

        # Filtro de nitidez (sharpen)
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        nítida = cv2.filter2D(equalizada, -1, kernel)

        # Binarização
        _, binarizada = cv2.threshold(nítida, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return binarizada

    except Exception as e:
        raise ValueError(f"Erro ao processar imagem: {e}")


def extrair_texto_da_imagem(imagem: np.ndarray) -> str:
    """Executa o OCR na imagem usando Tesseract."""
    config = r'--oem 3 --psm 6 -l por'
    return pytesseract.image_to_string(imagem, config=config)


def limpar_texto_ocr(texto: str) -> str:
    """Corrige erros comuns de OCR."""
    substituicoes = {
        "ONPJ": "CNPJ",
        "Docunento": "Documento",
        "Conssunidor": "Consumidor",
        "EletroL": "Eletrônica",
        "VirUnit": "VlrUnit",
        "ViCTotol": "VlrTotal",
        "TOTALABS": "TOTAL",
        "REDNEAA": "REDEMAIS",
    }

    for errado, certo in substituicoes.items():
        texto = texto.replace(errado, certo)

    return texto


def extrair_campos_nota(texto: str) -> dict:
    """Extrai CNPJ, data, valor e itens da nota a partir do texto limpo."""
    campos = {}

    # CNPJ
    cnpj = re.search(r'(\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})', texto)
    if cnpj:
        campos["CNPJ"] = cnpj.group(1)

    # Data de emissão
    data = re.search(r'(\d{2}/\d{2}/\d{4})', texto)
    if data:
        campos["Data de Emissão"] = data.group(1)

    # Valor total da nota
    total = re.search(r'VALOR\s+TOTAL\s+(R\$)?\s*[;:=-]?\s*([\d]+[.,]\d{2})', texto, re.IGNORECASE)
    if total:
        campos["Valor Total"] = total.group(2)

    # Itens vendidos (código, nome, quantidade, valor unitário, total item)
    itens = re.findall(
        r'(\d{8,13})\s+(.+?)\s+(\d+)\s+\w+\s+x\s+([\d.,]+)\s+([\d.,]+)',
        texto
    )
    if itens:
        campos["Itens"] = []
        for i, item in enumerate(itens, 1):
            campos["Itens"].append({
                "Item Nº": i,
                "Código": item[0],
                "Nome": item[1].strip(),
                "Quantidade": item[2],
                "Valor Unitário": item[3],
                "Valor Total Item": item[4]
            })

    return campos


def mostrar_resultados(campos: dict):
    """Exibe os campos extraídos de maneira organizada."""
    print("\n===== RESULTADOS EXTRAÍDOS =====")
    for chave, valor in campos.items():
        if chave == "Itens":
            print("\n📦 Itens da Nota:")
            for item in valor:
                for k, v in item.items():
                    print(f"   {k}: {v}")
                print("   ----------------------------")
        else:
            print(f"{chave}: {valor}")
    print("================================\n")


def processar_comprovante():
    """Pipeline completo: seleção, OCR, extração e exibição."""
    try:
        path = selecionar_imagem()
        if not path:
            print("Nenhum arquivo selecionado.")
            return

        imagem = preprocessar_imagem(path)
        texto_bruto = extrair_texto_da_imagem(imagem)
        texto_limpo = limpar_texto_ocr(texto_bruto)
        campos = extrair_campos_nota(texto_limpo)
        mostrar_resultados(campos)

    except Exception as e:
        print(f"Erro ao processar o comprovante: {e}")

