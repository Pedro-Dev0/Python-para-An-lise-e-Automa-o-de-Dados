import cv2
import pytesseract
import os
import csv
import pyautogui
import subprocess

# --- 1. CONFIGURAÇÕES INICIAIS ---
# Caminho do motor de leitura (OCR)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Onde estão as tuas fotos e onde salvar o relatório
PASTA_ORIGEM = r'\\servidor\Dados\ADMINISTRATIVO\LIVROS DE NOTAS\Digitalizacao cartorio\0 a 999\Livro_81_P_REFAZER' 
ARQUIVO_CSV = 'relatorio_final_livros.csv'

# --- 2. FUNÇÃO DE ANÁLISE TÉCNICA ---
def analisar_foto(caminho):
    img = cv2.imread(caminho)
    if img is None:
        return None

    # Converte para cinza para melhor processamento
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # A. Identifica se tem 1 ou 2 páginas pela proporção (Largura / Altura)
    h, w = cinza.shape
    proporcao = w / h
    qtd_paginas = "2 Paginas" if proporcao > 1.8 else "1 Pagina"

    # B. Identifica a Nitidez (Foco)
    # Score abaixo de 80 costuma indicar imagem borrada
    score_foco = cv2.Laplacian(cinza, cv2.CV_64F).var()
    
    # C. Tenta ler o texto (OCR) para ver se está legível
    # Giramos 90 graus porque tiraste a foto com o telemóvel deitado
    img_girada = cv2.rotate(cinza, cv2.ROTATE_90_CLOCKWISE)
    texto = pytesseract.image_to_string(img_girada, lang='por')
    
    # Define a qualidade baseada no foco e na quantidade de texto lido
    if score_foco > 80 and len(texto.strip()) > 40:
        qualidade = "BOA"
    else:
        qualidade = "RUIM (Revisar)"

    return {
        "paginas": qtd_paginas,
        "qualidade": qualidade,
        "score": round(score_foco, 2)
    }

# --- 3. EXECUÇÃO E REVISÃO VISUAL ---
print("--- INICIANDO TRABALHO DE CAMPO ---")

# Criar a planilha
with open(ARQUIVO_CSV, 'w', newline='', encoding='utf-8') as f:
    escritor = csv.writer(f)
    escritor.writerow(['Nome do Arquivo', 'Quantidade de Paginas', 'Qualidade da Imagem'])

    # Percorrer todas as fotos da pasta
    for nome_arquivo in os.listdir(PASTA_ORIGEM):
        if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            caminho_completo = os.path.join(PASTA_ORIGEM, nome_arquivo)
            
            # Realiza a análise
            resultado = analisar_foto(caminho_completo)
            
            if resultado:
                # Salva na planilha
                escritor.writerow([nome_arquivo, resultado['paginas'], resultado['qualidade']])
                print(f"Analisado: {nome_arquivo} | Status: {resultado['qualidade']}")

                # SE A QUALIDADE FOR RUIM, O PYAUTOGUI INTERVÉM
                if resultado['qualidade'] == "RUIM (Revisar)":
                    print(f"!!! Abrindo {nome_arquivo} para verificação manual...")
                    
                    # Abre a imagem no visualizador padrão do Windows
                    os.startfile(caminho_completo)
                    
                    # Cria um alerta na tela
                    resposta = pyautogui.confirm(
                        text=f"O arquivo {nome_arquivo} parece ter problemas.\n"
                             f"Qualidade: {resultado['qualidade']}\n\n"
                             f"Deseja continuar a análise dos próximos?",
                        title="Revisão Manual Necessária",
                        buttons=['Continuar', 'Parar']
                    )
                    
                    if resposta == 'Parar':
                        print("Análise interrompida pelo utilizador.")
                        break

print(f"\n--- FIM! Relatório disponível em: {ARQUIVO_CSV} ---")