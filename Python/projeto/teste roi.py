import cv2
import os
import csv
import time
import re
import pytesseract
import numpy as np

# --- CONFIGURAÇÃO ---
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
PASTA_FOTOS = r'\\servidor\Dados\ADMINISTRATIVO\LIVROS DE NOTAS\Digitalizacao cartorio\0 a 999\Livro_75_P_REFAZER'
LIMITE_FOCO = 15 # Mais tolerante para livros muito antigos

def natural_sort(l): 
    return sorted(l, key=lambda x: [int(c) if c.isdigit() else c.lower() for c in re.split('([0-9]+)', x)])

def limpar_e_ler(roi):
    """Limpeza pesada para eliminar ruídos de papel velho"""
    if roi is None or roi.size == 0: return None
    
    # 1. Escala de cinza e aumento de tamanho (ajuda o OCR em números pequenos)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # 2. Filtro de Mediana para remover 'pontinhos' pretos do papel velho
    gray = cv2.medianBlur(gray, 3)
    
    # 3. Binarização Adaptativa (separa tinta do fundo manchado)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # 4. Operação Morfológica para 'engrossar' os números e conectar traços falhos
    kernel = np.ones((2,2), np.uint8)
    thresh = cv2.dilate(thresh, kernel, iterations=1)

    # Configuração OCR focada em números (PSM 8 é para 'palavras' isoladas)
    config = '--psm 8 -c tessedit_char_whitelist=0123456789'
    texto = pytesseract.image_to_string(thresh, config=config).strip()
    
    num = re.sub(r'\D', '', texto)
    # Validação: números de página em cartório raramente passam de 4 dígitos (0-9999)
    return int(num) if (num and 1 <= len(num) <= 4) else None

def auditoria_recalibrada():
    nome_livro = os.path.basename(PASTA_FOTOS)
    caminho_csv = os.path.join(PASTA_FOTOS, f"Resumo_Auditoria_{nome_livro}.csv")
    
    arquivos = natural_sort([f for f in os.listdir(PASTA_FOTOS) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    
    dados = []
    ultimo_num_confirmado = 0
    fotos_vazias_seguidas = 0
    inicio = time.time()

    print(f"Auditando Livro: {nome_livro} | {len(arquivos)} imagens.")

    for nome in arquivos:
        img = cv2.imread(os.path.join(PASTA_FOTOS, nome))
        if img is None: continue

        h, w = img.shape[:2]
        
        # FOCO: Cálculo ultra rápido no centro
        centro = img[int(h*0.25):int(h*0.75), int(w*0.25):int(w*0.75)]
        score_foco = cv2.Laplacian(cv2.cvtColor(centro, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var()
        
        # ROIs: Cantos superiores (ignora os 2% da bordinha para evitar sombras do scanner)
        margem_h = int(h * 0.02)
        margem_w = int(w * 0.02)
        topo = int(h * 0.12)
        lateral = int(w * 0.15)
        
        c_esq = img[margem_h:topo, margem_w:lateral]
        c_dir = img[margem_h:topo, w-lateral:w-margem_w]
        
        # Tenta ler nos dois cantos
        num_lido = limpar_e_ler(c_dir) or limpar_e_ler(c_esq)
        
        status = "OK"
        alerta = ""

        # LÓGICA DE SEQUÊNCIA ANTI-FALSO POSITIVO
        if num_lido:
            # Se o número lido for menor ou igual ao anterior, pode ser erro de OCR ou página repetida
            if ultimo_num_confirmado > 0:
                if num_lido > ultimo_num_confirmado + 2:
                    status = "VERIFICAR"
                    alerta = f"Pulo suspeito: saltou de {ultimo_num_confirmado} para {num_lido}"
                elif num_lido <= ultimo_num_confirmado:
                    # Se o OCR leu '2' em vez de '28', ignoramos para não sujar o relatório
                    if num_lido < (ultimo_num_confirmado - 5):
                         num_lido = None # Desconsidera leitura bizarra
                    else:
                        status = "VERIFICAR"
                        alerta = "Página repetida ou erro de leitura"
            
            if num_lido: ultimo_num_confirmado = num_lido
            fotos_vazias_seguidas = 0
        else:
            fotos_vazias_seguidas += 1
            if fotos_vazias_seguidas > 2:
                status = "VERIFICAR"
                alerta = "Sequência de páginas sem numeração"

        if score_foco < LIMITE_FOCO:
            status = "BORRADA"
            alerta += " | Imagem sem nitidez"

        dados.append([nome, num_lido if num_lido else "---", status, alerta])

    # Salva o relatório na pasta do livro
    with open(caminho_csv, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Arquivo', 'Pagina_Lida', 'Status_Final', 'Observacoes'])
        w.writerows(dados)

    print(f"Concluído em {time.time()-inicio:.1f}s. Arquivo: {os.path.basename(caminho_csv)}")

if __name__ == "__main__":
    auditoria_recalibrada()