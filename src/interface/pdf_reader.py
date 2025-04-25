"""
pdf_reader.py - Conversão de PDFs em imagem e leitura de QR Codes
"""

import cv2
import numpy as np
import easygui
from pdf2image import convert_from_path
from core.detection import detectar_qr_em_frame
from core.utils import salvar_log
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def selecionar_pdf() -> str:
    """
    Abre uma janela de seleção de arquivos para escolher um PDF.

    Returns:
        str: Caminho do arquivo selecionado ou string vazia se cancelado.
    """
    root = tk.Tk()
    root.lift()            # Garante que a janela fique em foco
    root.attributes('-topmost', True)  # Coloca no topo
    root.after_idle(root.attributes, '-topmost', False)  # Remove "always on top" depois

    caminho = filedialog.askopenfilename(
        parent=root,
        title="Selecione o arquivo PDF",
        filetypes=[("PDF files", "*.pdf")]
    )

    root.destroy()
    return caminho


def usar_pdf(poppler_path: str):
    filepath = selecionar_pdf()
    if not filepath:
        print("Nenhum arquivo selecionado.")
        return

    try:
        print("➡️ Convertendo PDF para imagem...")
        paginas = convert_from_path(filepath, dpi=400, poppler_path=poppler_path)
        pagina = paginas[0]

        frame = cv2.cvtColor(np.array(pagina), cv2.COLOR_RGB2BGR)

        # Redimensiona imagem se for muito grande
        if frame.shape[1] > 1200:
            frame = cv2.resize(frame, (1200, int(frame.shape[0] * 1200 / frame.shape[1])))

        frame, dados_detectados = detectar_qr_em_frame(frame)

        cv2.imshow("QR Code - PDF", frame)
        print("Pressione qualquer tecla para continuar ou aguarde 5 segundos...")
        cv2.waitKey(5000)
        cv2.destroyAllWindows()

        salvar_log(dados_detectados)

    except Exception as e:
        print(f"Erro ao processar PDF: {e}")
