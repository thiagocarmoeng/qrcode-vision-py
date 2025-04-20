import cv2
from googletrans import Translator
import pyautogui
import easygui
import numpy as np
import datetime
import os
from pdf2image import convert_from_path
import ctypes
from pyzbar.pyzbar import decode
import threading
cache_traducoes = {}
# Inicializa o detector de QR Code do OpenCV
detector = cv2.QRCodeDetector()

def traduzir_texto(texto, idioma_destino='pt'):
    """Traduz o texto detectado para o idioma desejado."""
    tradutor = Translator()
    traducao = tradutor.translate(texto, dest=idioma_destino)
    return traducao.text

def traduzir_texto_async(texto):
    try:
        tradutor = Translator()
        traducao = tradutor.translate(texto, dest='pt').text
        cache_traducoes[texto] = traducao
        print(f"✅ Tradução concluída: {traducao}")
    except Exception as e:
        print(f"❌ Erro na tradução: {e}")
        cache_traducoes[texto] = "Erro"

def salvar_log(dados_detectados):
    """Salva os dados detectados e traduzidos em um arquivo de log .txt."""
    if not dados_detectados:
        return
    
    if not os.path.exists('logs'):
        os.makedirs('logs')

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/deteccao_qrcode_{timestamp}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        for original, traducao in dados_detectados:
            f.write(f"Original: {original}\n")
            f.write(f"Tradução: {traducao}\n")
            f.write("="*50 + "\n")

    print(f"\n🔵 Resultados salvos em: {filename}")

# def detectar_qr_em_frame(frame):
#     """Detecta e traduz QR Codes em um frame usando pyzbar, com reforço de imagem."""
#     dados_detectados = []

#     frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Melhorar contraste
#     frame_cinza = cv2.equalizeHist(frame_cinza)

#     # Aumentar nitidez artificialmente
#     kernel_sharpening = np.array([[-1,-1,-1],
#                                   [-1, 9,-1],
#                                   [-1,-1,-1]])
#     frame_cinza = cv2.filter2D(frame_cinza, -1, kernel_sharpening)

#     # Detectar com pyzbar
#     qrcodes = decode(frame_cinza)

#     if not qrcodes:
#         print("Nenhum QR Code encontrado no frame.")
#     else:
#         for qr in qrcodes:
#             pontos = np.array([qr.polygon], np.int32)
#             pontos = pontos.reshape((-1, 1, 2))
#             cv2.polylines(frame, [pontos], True, (0, 255, 0), 2)

#             dados = qr.data.decode('utf-8')
#             print(f"✅ QR Detectado: {dados}")

#             traducao = traduzir_texto(dados)

#             dados_detectados.append((dados, traducao))

#             x, y, w, h = qr.rect
#             cv2.putText(frame, f"Original: {dados}", (x, y - 30),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#             cv2.putText(frame, f"Traducao: {traducao}", (x, y - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

#     return frame, dados_detectados

def traduzir_texto_async(texto):
    """Função que traduz texto de forma assíncrona e salva no cache."""
    try:
        tradutor = Translator()
        traducao = tradutor.translate(texto, dest='pt').text
        cache_traducoes[texto] = traducao
        print(f"✅ Tradução concluída: {traducao}")
    except Exception as e:
        print(f"❌ Erro na tradução: {e}")
        cache_traducoes[texto] = "Erro"

def detectar_qr_em_frame(frame):
    """Detecta e traduz QR Codes em um frame usando pyzbar, com reforço de imagem."""
    dados_detectados = []

    frame_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Melhorar contraste
    frame_cinza = cv2.equalizeHist(frame_cinza)

    # Aumentar nitidez artificialmente
    kernel_sharpening = np.array([[-1,-1,-1],
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
    frame_cinza = cv2.filter2D(frame_cinza, -1, kernel_sharpening)
    frame_cinza = cv2.equalizeHist(frame_cinza)
    frame_cinza = cv2.GaussianBlur(frame_cinza, (5, 5), 0)

    qrcodes = decode(frame_cinza)


    if not qrcodes:
        print("Nenhum QR Code encontrado no frame.")
    else:
        for qr in qrcodes:
            try:
                dados = qr.data.decode('utf-8')

                if dados:
                    print(f"✅ QR Detectado: {dados}")

                    # Desenhar contorno
                    pontos = np.array([qr.polygon], np.int32)
                    pontos = pontos.reshape((-1, 1, 2))
                    cv2.polylines(frame, [pontos], True, (0, 255, 0), 2)

                    # Pegar coordenadas para desenhar texto
                    x, y, w, h = qr.rect

                    # Iniciar tradução em background se ainda não estiver no cache
                    if dados not in cache_traducoes:
                        threading.Thread(target=traduzir_texto_async, args=(dados,)).start()

                    # Pega tradução pronta ou mostra "Traduzindo..."
                    traducao = cache_traducoes.get(dados, "Traduzindo...")

                    # Escrever os textos na imagem
                    cv2.putText(frame, f"Original: {dados}", (x, y - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    cv2.putText(frame, f"Traducao: {traducao}", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    # Opcionalmente, registrar o dado detectado
                    dados_detectados.append((dados, traducao))

                else:
                    print("⚠️ QR Code detectado sem dados (vazio).")

            except Exception as e:
                print(f"❌ Erro ao processar QR Code: {e}")

    return frame, dados_detectados


def usar_camera():
    cap = cv2.VideoCapture(0)
    print("Usando câmera... Pressione 'q' para sair.")

    dados_totais = []

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao acessar a câmera.")
            break

        frame, dados = detectar_qr_em_frame(frame)
        dados_totais.extend(dados)

        cv2.imshow("Leitor de QR Code (Câmera)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    salvar_log(dados_totais)

def usar_tela():
    """Captura QR Codes de um screenshot da tela."""
    print("Tirando screenshot da tela...")
    screenshot = pyautogui.screenshot()
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    frame, dados_detectados = detectar_qr_em_frame(frame)

    cv2.imshow("Leitor de QR Code (Tela)", frame)
    print("▶️ Pressione qualquer tecla para continuar ou aguarde 5 segundos...")
    key = cv2.waitKey(5000)  # Timeout de 5 segundos
    cv2.destroyAllWindows()

    salvar_log(dados_detectados)

def usar_arquivo():
    """Seleciona e lê um arquivo de imagem para detectar QR Codes."""
    filepath = easygui.fileopenbox(title="Selecione uma imagem de QR Code",
                                   filetypes=["*.png", "*.jpg", "*.jpeg"])
    if not filepath:
        print("Nenhum arquivo selecionado.")
        return

    frame = cv2.imread(filepath)

    if frame is None:
        print("Erro: Não foi possível carregar a imagem. Verifique o formato do arquivo.")
        return

    frame, dados_detectados = detectar_qr_em_frame(frame)

    cv2.imshow("Leitor de QR Code (Arquivo)", frame)
    print("▶️ Pressione qualquer tecla para continuar ou aguarde 5 segundos...")
    key = cv2.waitKey(5000)
    cv2.destroyAllWindows()

    salvar_log(dados_detectados)

def usar_pdf():
    """Seleciona um arquivo PDF, converte a página em imagem e detecta QR Code usando pyzbar."""
    filepath = easygui.fileopenbox(title="Selecione o arquivo PDF",
                                   filetypes=["*.pdf"])
    if not filepath:
        print("Nenhum arquivo selecionado.")
        return

    path_poppler = r"C:\Users\thiag\OneDrive\Área de Trabalho\visão computacional\Proj - identificação de QRCode\poppler-24.08.0\Library\bin"

    try:
        paginas = convert_from_path(filepath, dpi=400, poppler_path=path_poppler)
        pagina = paginas[0]

        frame = cv2.cvtColor(np.array(pagina), cv2.COLOR_RGB2BGR)

        dados_detectados = []

        # Usar pyzbar para detectar o QR Code
        qrcodes = decode(frame)

        if not qrcodes:
            print("Nenhum QR Code encontrado na imagem!")
        else:
            for qr in qrcodes:
                pontos = np.array([qr.polygon], np.int32)
                pontos = pontos.reshape((-1, 1, 2))
                cv2.polylines(frame, [pontos], True, (0, 255, 0), 2)

                dados = qr.data.decode('utf-8')
                traducao = traduzir_texto(dados)

                dados_detectados.append((dados, traducao))

                x, y, w, h = qr.rect
                cv2.putText(frame, f"Original: {dados}", (x, y - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                cv2.putText(frame, f"Traducao: {traducao}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow("Leitor de QR Code (PDF)", frame)
        print("▶️ Pressione qualquer tecla para continuar ou aguarde 5 segundos...")
        cv2.waitKey(5000)
        cv2.destroyAllWindows()

        salvar_log(dados_detectados)

    except Exception as e:
        print(f"Erro ao processar PDF: {e}")

def menu():
    """Menu principal para escolher a fonte."""
    while True:
        print("\n===== Menu de Operações =====")
        print("[1] Ler QR Code da Câmera")
        print("[2] Capturar QR Code da Tela")
        print("[3] Ler QR Code de um Arquivo de Imagem")
        print("[4] Ler QR Code de um Arquivo PDF")
        print("[0] Sair")

        escolha = input("Escolha a opção: ")

        if escolha == '1':
            usar_camera()
        elif escolha == '2':
            usar_tela()
        elif escolha == '3':
            usar_arquivo()
        elif escolha == '4':
            usar_pdf()
        elif escolha == '0':
            print("Encerrando programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
