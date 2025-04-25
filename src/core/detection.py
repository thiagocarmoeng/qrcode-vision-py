"""
detection.py - Módulo de detecção e overlay de QR Codes
"""

import cv2
import numpy as np
from pyzbar.pyzbar import decode
import threading
from core.translation import traduzir_texto_async, cache_traducoes


def detectar_qr_em_frame(frame):
    """
    Detecta QR Codes no frame, desenha os contornos e exibe a tradução.

    Args:
        frame (np.ndarray): Imagem de entrada (frame da câmera, tela ou arquivo).

    Returns:
        tuple: (frame com anotações, lista de tuplas (texto original, tradução))
    """
    dados_detectados = []

    # Pré-processamento da imagem
    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_cinza = cv2.equalizeHist(frame_cinza)
    frame_cinza = cv2.GaussianBlur(frame_cinza, (5, 5), 0)
    frame_cinza = cv2.filter2D(
        frame_cinza, -1,
        np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    )

    qrcodes = decode(frame_cinza)

    for qr in qrcodes:
        try:
            dados = qr.data.decode('utf-8')
            if not dados:
                continue

            print(f"QR Detectado: {dados}")

            x, y, w, h = qr.rect
            pontos = np.array([qr.polygon], np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [pontos], True, (0, 255, 0), 2)

            if dados not in cache_traducoes:
                threading.Thread(target=traduzir_texto_async, args=(dados,)).start()

            traducao = cache_traducoes.get(dados, "Traduzindo...")

            cv2.putText(frame, f"Original: {dados}", (x, y - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.putText(frame, f"Tradução: {traducao}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            dados_detectados.append((dados, traducao))

        except Exception as e:
            print(f"Erro ao processar QR Code: {e}")

    return frame, dados_detectados
