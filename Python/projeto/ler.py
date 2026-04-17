import cv2
import os
import time

# --- CONFIGURAÇÃO ---
PASTA_FOTOS = r'\\servidor\Dados\ADMINISTRATIVO\LIVROS DE NOTAS\Digitalizacao cartorio\0 a 999\Livro_81_P_REFAZER'
TEMPO_SLAIDE = 0.3  # Ainda mais rápido: 0.3 segundos por foto (ajustável)
LIMITE_FOCO = 20    # ALTA TOLERÂNCIA: Menos que isso é realmente um borrão total

def varredura_turbo():
    # 1. Lista e Ordena os arquivos
    arquivos = sorted([f for f in os.listdir(PASTA_FOTOS) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    if not arquivos:
        print("Pasta vazia!")
        return

    print(f"Iniciando análise de {len(arquivos)} imagens...")
    cv2.namedWindow("REVISAO EXPRESSA", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("REVISAO EXPRESSA", 1000, 800)

    inicio_total = time.time()

    for nome in arquivos:
        caminho = os.path.join(PASTA_FOTOS, nome)
        img = cv2.imread(caminho)

        if img is not None:
            # --- PROCESSAMENTO ULTRA RÁPIDO ---
            h, w = img.shape[:2]
            cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Cálculo de nitidez (Laplaciano) - Instantâneo
            score = cv2.Laplacian(cinza, cv2.CV_64F).var()
            
            # Detecção de páginas (1 ou 2)
            paginas = "2 Pags" if (w / h) > 1.4 else "1 Pag"
            
            # Status com tolerância
            status = "OK" if score > LIMITE_FOCO else "BORRADO"
            cor = (0, 255, 0) if status == "OK" else (0, 0, 255)

            # --- VISUALIZAÇÃO ---
            # Escreve info direto na imagem
            info = f"[{nome}] | {paginas} | Foco: {int(score)} | {status}"
            cv2.putText(img, info, (40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, cor, 3)
            
            cv2.imshow("REVISAO EXPRESSA", img)

            # Controla a velocidade (0.3s) ou para no ESC
            if cv2.waitKey(int(TEMPO_SLAIDE * 1000)) & 0xFF == 27:
                break
        else:
            print(f"Erro no arquivo: {nome}")

    tempo_final = time.time() - inicio_total
    cv2.destroyAllWindows()
    print(f"\n--- CONCLUÍDO ---")
    print(f"Tempo total: {tempo_final:.2f} segundos para {len(arquivos)} fotos.")

if __name__ == "__main__":
    varredura_turbo()