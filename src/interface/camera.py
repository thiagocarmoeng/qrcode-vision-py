"""
camera.py - Captura QR Codes usando a webcam em tempo real
"""

import cv2
from core.detection import detectar_qr_em_frame
from core.utils import salvar_log


def usar_camera():
    """
    Captura contínua de frames da webcam, com detecção e tradução de QR Codes.

    Exibe os resultados em tempo real na tela e salva os dados detectados ao final.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao acessar a câmera.")
        return

    print("Usando câmera... Pressione 'q' para sair.")
    dados_totais = []

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Frame inválido capturado da câmera.")
                break

            frame, dados = detectar_qr_em_frame(frame)
            dados_totais.extend(dados)

            cv2.imshow("QR Code - Câmera", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        salvar_log(dados_totais)
