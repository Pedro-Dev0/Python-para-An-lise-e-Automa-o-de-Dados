import cv2
import os
import time

# --- CONFIGURAÇÃO ---
PASTA_FOTOS = r'C:\Users\Malleus\Downloads\verja'
TEMPO_EXIBICAO = 1.5  # Meio segundo por foto

def revisao_ultra_rapida():
    # 1. Pega a lista de imagens
    arquivos = [f for f in os.listdir(PASTA_FOTOS) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.jfif'))]
    
    if not arquivos:
        print("Nenhuma imagem encontrada!")
        return

    print(f"Total: {len(arquivos)} imagens.")
    print("Iniciando exibição... Pressione 'ESC' para parar.")

    # 2. Cria uma janela que pode ser redimensionada
    cv2.namedWindow("Revisao Rapida", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Revisao Rapida", 800, 600) # Ajuste o tamanho aqui

    for nome in arquivos:
        caminho = os.path.join(PASTA_FOTOS, nome)
        img = cv2.imread(caminho)

        if img is not None:
            # Escreve o nome do arquivo na imagem para você saber qual é
            cv2.putText(img, nome, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Mostra a imagem
            cv2.imshow("Revisao Rapida", img)

            # Espera o tempo definido (0.5s)
            # Se você apertar a tecla 'ESC' (código 27), o programa para
            if cv2.waitKey(int(TEMPO_EXIBICAO * 1000)) & 0xFF == 27:
                break
        else:
            print(f"Erro ao carregar: {nome}")

    cv2.destroyAllWindows()
    print("Varredura finalizada.")

if __name__ == "__main__":
    revisao_ultra_rapida()