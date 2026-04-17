import cv2
import os
import csv
import time
import re  # Biblioteca para tratar a ordem dos números

# --- CONFIGURAÇÃO ---
PASTA_FOTOS = r'\\servidor\Dados\ADMINISTRATIVO\LIVROS DE NOTAS\Digitalizacao cartorio\0 a 999\Livro_81_P_REFAZER'
ARQUIVO_RELATORIO = 'relatorio_final_ordenado.csv'
LIMITE_FOCO_TOLERANTE = 20 

def chave_ordenacao_natural(texto):
    """ Função que ensina o Python a ordenar 1, 2, 10 em vez de 1, 10, 2 """
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', texto)]

def gerar_relatorio_perfeito():
    # 1. Lista os arquivos
    lista_bruta = [f for f in os.listdir(PASTA_FOTOS) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # 2. ORDENAÇÃO NATURAL (Aqui está o segredo!)
    arquivos = sorted(lista_bruta, key=chave_ordenacao_natural)
    
    if not arquivos:
        print("Pasta vazia!")
        return

    print(f"Analisando {len(arquivos)} imagens na ordem correta...")
    inicio_tempo = time.time()
    dados_final = []

    for nome in arquivos:
        caminho = os.path.join(PASTA_FOTOS, nome)
        img = cv2.imread(caminho)

        if img is not None:
            # Cálculo de Foco
            cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            score_foco = cv2.Laplacian(cinza, cv2.CV_64F).var()
            
            # Contagem de Páginas (Proporção)
            h, w = cinza.shape
            qtd_paginas = 2 if (w / h) > 1.4 else 1
            
            # Status e Erro
            if score_foco < LIMITE_FOCO_TOLERANTE:
                status = f"ERRO: Foco muito baixo ({int(score_foco)}) - Imagem Borrada"
            else:
                status = "OK"

            dados_final.append([nome, qtd_paginas, round(score_foco, 2), status])
        else:
            dados_final.append([nome, "N/A", 0, "ERRO: Arquivo não abre"])

    # 3. Salva o Relatório
    with open(ARQUIVO_RELATORIO, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f)
        escritor.writerow(['Arquivo', 'Pags Detectadas', 'Score Foco', 'Resultado'])
        escritor.writerows(dados_final)

    tempo_total = time.time() - inicio_tempo
    print(f"\n--- SUCESSO EM {tempo_total:.2f}s ---")
    print(f"O arquivo '{ARQUIVO_RELATORIO}' está pronto e ordenado!")

if __name__ == "__main__":
    gerar_relatorio_perfeito()