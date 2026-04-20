import os
import time
import subprocess
import pyautogui
from natsort import natsorted

# --- CONFIGURAÇÃO ---
PASTA_FOTOS = r'\\servidor\Dados\ADMINISTRATIVO\LIVROS DE NOTAS\Digitalizacao cartorio\0 a 999\Livro_75_P_REFAZER'
TEMPO_ESPERA = 0.6  # Velocidade máxima: 600 milissegundos

def revisao_modo_insano():
    # Ordenação natural garantida
    arquivos = natsorted([f for f in os.listdir(PASTA_FOTOS) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    
    if not arquivos:
        print("Pasta vazia!")
        return

    print("="*60)
    print(f"MODO INSANO ATIVADO: {TEMPO_ESPERA}s")
    print("MANTENHA O FOCO NA JANELA DA FOTO!")
    print("="*60)

    # Abre a primeira imagem
    primeira_foto = os.path.join(PASTA_FOTOS, arquivos[0])
    subprocess.Popen(f'start "" "{primeira_foto}"', shell=True)
    
    # Tempo para o visualizador carregar antes da sequência começar
    time.sleep(2.5)

    for i in range(1, len(arquivos)):
        # Mostra o progresso (pode haver um pequeno atraso no print devido à velocidade)
        print(f"Foto {i+1}/{len(arquivos)}", end="\r")
        
        # Intervalo de 0,6 segundos
        time.sleep(TEMPO_ESPERA)
        
        # Envia o comando de seta para a direita
        pyautogui.press('right')

    print("\n\n" + "="*60)
    print("MISSÃO CUMPRIDA!")
    print("="*60)

if __name__ == "__main__":
    try:
        # Remove qualquer atraso entre comandos do pyautogui
        pyautogui.PAUSE = 0.0
        revisao_modo_insano()
    except Exception as e:
        print(f"\nParado: {e}")