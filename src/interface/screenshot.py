"""
screenshot.py - Captura e leitura de QR Codes a partir de um screenshot da tela
"""

import cv2
import numpy as np
import pyautogui
from core.detection import detectar_qr_em_frame
from core.utils import salvar_log

def usar_tela() -> None:
    """
    Captura um screenshot da tela, detecta e traduz QR Codes presentes na imagem.

    Exibe o resultado com as anotações e salva os dados em arquivo de log.
    """
    print("📸 Capturando screenshot da tela...")
    imagem_tela = pyautogui.screenshot()

    # Converte para formato OpenCV (BGR)
    frame = cv2.cvtColor(np.array(imagem_tela), cv2.COLOR_RGB2BGR)

    # Aplica detecção e tradução
    frame, dados_detectados = detectar_qr_em_frame(frame)

    # Exibe resultado
    cv2.imshow("QR Code - Tela", frame)
    print("▶️ Pressione qualquer tecla para continuar ou aguarde 5 segundos...")
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

    # Salva dados detectados
    salvar_log(dados_detectados)

