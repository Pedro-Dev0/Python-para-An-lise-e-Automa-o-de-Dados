import os
import cv2
import torch
import csv
import numpy as np
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from natsort import natsorted

# 1. SETUP IA
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Rodando em: {device}")

# Usando o modelo 'stage1' que é mais robusto para números e caracteres isolados
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-printed") 
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-small-printed").to(device)

PASTA_FOTOS = r'\\servidor\Dados\ADMINISTRATIVO\LIVROS DE NOTAS\Digitalizacao cartorio\0 a 999\Livro_542_P'
RELATORIO = os.path.join(PASTA_FOTOS, "AUDITORIA_FINAL.csv")

def limpar_imagem_extremo(img_cv):
    """ Foca no índice eliminando sombras e ruído de carimbo """
    alt, larg = img_cv.shape[:2]
    
    # Recorte GENEROSO para garantir que o índice esteja dentro (20% topo, 35% direita)
    recorte = img_cv[0:int(alt*0.20), int(larg*0.65):larg]
    
    # Converte para escala de cinza
    gray = cv2.cvtColor(recorte, cv2.COLOR_BGR2GRAY)
    
    # Aumenta o contraste (crucial para caneta fraca)
    alpha = 1.5 # Contraste
    beta = 10    # Brilho
    gray = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    
    # Binarização: Deixa o papel BRANCO PURO e a caneta PRETA
    # Isso remove 90% dos carimbos coloridos (azul/vermelho)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return Image.fromarray(thresh).convert("RGB")

def analisar_livro():
    arquivos = natsorted([f for f in os.listdir(PASTA_FOTOS) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    
    with open(RELATORIO, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['ARQUIVO', 'INDICE', 'QUALIDADE'])

        for nome in arquivos:
            caminho = os.path.join(PASTA_FOTOS, nome)
            img = cv2.imread(caminho)
            if img is None: continue

            # 1. Qualidade (Foco) - Se for < 30, está muito ruim
            blur_score = cv2.Laplacian(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
            qualidade = "OK" if blur_score > 35 else "BORRADA"

            # 2. Processamento de Imagem + IA
            try:
                img_ia = limpar_imagem_extremo(img)
                pixel_values = processor(img_ia, return_tensors="pt").pixel_values.to(device)
                
                # Gera o texto
                generated_ids = model.generate(pixel_values, max_new_tokens=10)
                texto = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
                
                # Filtra apenas dígitos
                indice = "".join(filter(str.isdigit, texto))
            except Exception as e:
                indice = "ERRO"

            print(f"Arquivo: {nome} | Índice: {indice} | Foco: {int(blur_score)}")
            writer.writerow([nome, indice, qualidade])

if __name__ == "__main__":
    analisar_livro()