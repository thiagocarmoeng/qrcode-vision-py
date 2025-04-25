"""
main.py - Programa principal para leitura de QR Codes e extração de dados de comprovantes
"""

from interface.camera import usar_camera
from interface.screenshot import usar_tela
from interface.file_input import usar_arquivo
from interface.pdf_reader import usar_pdf
from interface.comprovante_reader import processar_comprovante

# Caminho para o Poppler usado na leitura de PDFs
poppler_path = r"C:\Users\thiag\OneDrive\Área de Trabalho\visão computacional\Proj - identificação de QRCode\poppler-24.08.0\Library\bin"

def menu():
    """
    Menu principal para escolher a fonte de entrada de QR Codes ou comprovantes.
    """
    while True:
        print("\n===== Menu de Operações =====")
        print("[1] Ler QR Code da Câmera")
        print("[2] Capturar QR Code da Tela")
        print("[3] Ler QR Code de um Arquivo de Imagem")
        print("[4] Ler QR Code de um Arquivo PDF")
        print("[5] Ler Comprovante (Nota Fiscal via OpenCV)")
        print("[0] Sair")

        escolha = input("Escolha a opção: ")

        if escolha == '1':
            usar_camera()
        elif escolha == '2':
            usar_tela()
        elif escolha == '3':
            usar_arquivo()
        elif escolha == '4':
            usar_pdf(poppler_path)
        elif escolha == '5':
            processar_comprovante()
        elif escolha == '0':
            print("Encerrando programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
