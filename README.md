# QRCode Vision Py

QRCode Vision Py é um sistema desenvolvido em Python para a detecção, leitura e tradução de QR Codes a partir de múltiplas fontes, utilizando técnicas modernas de visão computacional.

O projeto é capaz de capturar QR Codes em tempo real via câmera, capturas de tela, imagens estáticas e arquivos PDF. A leitura é realizada com processamento prévio para otimizar contraste e nitidez, aumentando a robustez da detecção em ambientes variados.

A tradução do conteúdo dos QR Codes é realizada de maneira assíncrona, garantindo fluidez na operação, sem travamentos, mesmo durante o processamento de múltiplos códigos em sequência.

## Principais Funcionalidades
- Captura de QR Codes a partir de câmera, tela, imagens e PDFs.
- Pré-processamento de imagens (equalização de histograma e sharpening).
- Detecção de QR Codes com pyzbar.
- Tradução automática do conteúdo dos QR Codes com execução assíncrona (threads).
- Exibição dos resultados diretamente no vídeo com sobreposição dos textos "Original" e "Tradução".
- Salvamento automático dos resultados detectados em arquivos de log.
- Arquitetura modular e expansível para futuras melhorias.

## Tecnologias Utilizadas
- Python 3.11
- OpenCV
- pyzbar
- Googletrans
- pdf2image
- PyAutoGUI
- EasyGUI

## Possíveis Melhorias Futuras
- Exportação dos resultados em formato CSV.
- Integração com redes neurais para detecção avançada de QR Codes.
- Implementação de uma interface gráfica (GUI) para maior usabilidade.
- Suporte a super-resolução de imagens para leitura de QR Codes de baixa qualidade.

