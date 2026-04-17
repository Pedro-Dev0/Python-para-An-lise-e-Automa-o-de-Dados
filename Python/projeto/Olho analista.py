import cv2
import os
import csv
import time
import re

# --- CONFIGURAÇÃO ---
# Basta colar o caminho da pasta do livro aqui
PASTA_FOTOS = r'\\servidor\Dados\ADMINISTRATIVO\LIVROS DE NOTAS\Digitalizacao cartorio\0 a 999\Livro_75_P_REFAZER'
LIMITE_FOCO_TOLERANTE = 20 

def chave_ordenacao_natural(texto):
    """ Garante a ordem 1, 2, 3... 10, 11 em vez de 1, 10, 11, 2 """
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', texto)]

def gerar_relatorio_por_livro():
    # 1. Identifica o nome do livro pela pasta
    nome_do_livro = os.path.basename(PASTA_FOTOS)
    nome_arquivo_csv = f"Relatorio_Qualidade_{nome_do_livro}.csv"
    caminho_completo_csv = os.path.join(PASTA_FOTOS, nome_arquivo_csv)

    # 2. Lista e ordena os arquivos de forma natural
    lista_bruta = [f for f in os.listdir(PASTA_FOTOS) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    arquivos = sorted(lista_bruta, key=chave_ordenacao_natural)
    
    if not arquivos:
        print(f"Erro: Nenhuma imagem encontrada em {PASTA_FOTOS}")
        return

    print(f"Analizando: {nome_do_livro}")
    print(f"Total de imagens: {len(arquivos)}")
    
    inicio_tempo = time.time()
    dados_final = []

    # 3. Processamento Ultra Rápido
    for nome in arquivos:
        caminho_imagem = os.path.join(PASTA_FOTOS, nome)
        img = cv2.imread(caminho_imagem)

        if img is not None:
            # Cálculo de Foco (Nitidez)
            cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            score_foco = cv2.Laplacian(cinza, cv2.CV_64F).var()
            
            # Contagem de Páginas (Proporção da imagem)
            h, w = cinza.shape
            qtd_paginas = 2 if (w / h) > 1.4 else 1
            
            # Status com alta tolerância
            if score_foco < LIMITE_FOCO_TOLERANTE:
                status = f"ERRO: Foco muito baixo ({int(score_foco)})"
            else:
                status = "OK"

            dados_final.append([nome_do_livro, nome, qtd_paginas, round(score_foco, 2), status])
        else:
            dados_final.append([nome_do_livro, nome, "N/A", 0, "ERRO: Arquivo corrompido"])

    # 4. Salva o CSV dentro da própria pasta do livro
    with open(caminho_completo_csv, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerow(['Livro', 'Arquivo', 'Paginas', 'Score Foco', 'Status Final'])
        escritor.writerows(dados_final)

    tempo_total = time.time() - inicio_tempo
    print(f"\n--- FINALIZADO EM {tempo_total:.2f}s ---")
    print(f"Relatório salvo em: {caminho_completo_csv}")

if __name__ == "__main__":
    gerar_relatorio_por_livro()