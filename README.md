# QRCode Vision Py

Este projeto foi desenvolvido com o objetivo de integrar tecnologias de visão computacional e OCR (Reconhecimento Óptico de Caracteres) para **detecção de QR Codes e leitura de comprovantes/Notas Fiscais**.

A solução é modular, escrita em Python, e utiliza bibliotecas especializadas para processar imagens e extrair informações de forma precisa, mesmo em ambientes ruidosos.

---

## 🚀 Funcionalidades

- Leitura de **QR Codes** via:
  - 📷 Câmera
  - 📄 Arquivos de imagem
  - 🖥️ Captura de tela
  - 📑 Arquivos PDF
- Tradução automática do conteúdo lido (Google Translate)
- Leitura de **comprovantes e notas fiscais**, com extração de:
  - CNPJ
  - Data de emissão
  - Valor total
  - Itens vendidos (código, nome, quantidade, valor unitário e total)
- Geração de logs com os dados extraídos

---

## 🧠 Tecnologias Empregadas

| Tecnologia      | Finalidade                                      |
|-----------------|--------------------------------------------------|
| Python 3.x      | Linguagem principal                             |
| OpenCV          | Processamento de imagens                        |
| PyTesseract     | OCR com suporte multilíngue                     |
| Tesseract-OCR   | Engine de reconhecimento ótico local            |
| Googletrans     | Tradução automática de conteúdo                 |
| pdf2image       | Conversão de páginas de PDF para imagem         |
| Tkinter         | Interface gráfica para seleção de arquivos      |
| Regex (re)      | Extração estruturada de texto pós-OCR           |

---

## 🛠️ Instalação

### 1. Clone o repositório:
```bash
git clone https://github.com/thiagocarmoeng/qrcode-vision-py.git
cd qrcode-vision-py
```

### 2. Crie o ambiente virtual e ative:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 4. Instale o [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract):
- Windows: Baixe o instalador e adicione o caminho ao `PATH` ou configure diretamente no código.

---

## ▶️ Como Usar

### Modo interativo (menu no terminal):
```bash
python src/main.py
```

Você poderá:
- Ler QR Code por câmera
- Selecionar uma imagem da tela ou do disco
- Processar comprovantes de forma automatizada

---

## 📂 Estrutura de Diretórios

```
src/
├── core/
│   ├── detection.py
│   ├── translation.py
│   ├── utils.py
├── interface/
│   ├── camera.py
│   ├── file_input.py
│   ├── screenshot.py
│   ├── pdf_reader.py
│   ├── comprovante_reader.py
├── main.py
```

---

## 📈 Melhorias Futuras

- 🔍 Aplicar IA com LayoutLMv3 ou Donut para leitura sem OCR
- 💬 Extração semântica baseada em aprendizado de máquina
- 🖼 Overlay visual interativo para marcação dos campos na imagem
- 💾 Exportação para `.csv` ou integração com banco de dados
- 🌐 Interface Web com Streamlit ou Flask

---

## 👨‍💻 Autor

Desenvolvido por **Thiago do Carmo**  
[LinkedIn](https://www.linkedin.com/in/thiago-augusto-do-carmo/) | [GitHub](https://github.com/thiagocarmoeng)

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
