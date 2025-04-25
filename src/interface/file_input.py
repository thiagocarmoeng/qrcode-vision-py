"""
file_input.py - Leitura de imagens locais (.png, .jpg, .jpeg) para detecção de QR Codes
"""

import cv2
import easygui
from core.detection import detectar_qr_em_frame
from core.utils import salvar_log


def usar_arquivo():
    """
    Permite ao usuário selecionar uma imagem do disco para análise de QR Code.

    Exibe o resultado com overlay do conteúdo detectado e salva os dados em log.
    """
    filepath = easygui.fileopenbox(
        title="Selecione uma imagem de QR Code",
        filetypes=["*.png", "*.jpg", "*.jpeg"]
    )

    if not filepath:
        print("Nenhum arquivo selecionado.")
        return

    frame = cv2.imread(filepath)

    if frame is None:
        print("Erro: Não foi possível carregar a imagem. Verifique o formato do arquivo.")
        return

    frame, dados_detectados = detectar_qr_em_frame(frame)

    cv2.imshow("QR Code - Arquivo", frame)
    print("Pressione qualquer tecla para continuar ou aguarde 5 segundos...")
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

    salvar_log(dados_detectados)
