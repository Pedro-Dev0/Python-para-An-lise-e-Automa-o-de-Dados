import os
import time
import subprocess
import pyautogui
import zipfile
import shutil
from natsort import natsorted

# --- CONFIGURAÇÃO ---
CAMINHO_ZIP = r'\\DESKTOP-1UFML41\Digitalizacao\Enviados-migracao\_T\Livro_1066_T(1).zip'
PASTA_TEMP = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'temp_revisao_insana')
TEMPO_ESPERA = 0.6 

def revisao_modo_insano():
    if os.path.exists(PASTA_TEMP):
        shutil.rmtree(PASTA_TEMP)
    os.makedirs(PASTA_TEMP)

    print("Extraindo imagens para processamento local...")
    with zipfile.ZipFile(CAMINHO_ZIP, 'r') as z:
        imagens = [f for f in z.namelist() if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        for img in imagens:
            z.extract(img, PASTA_TEMP)

    arquivos = natsorted([f for f in os.listdir(PASTA_TEMP) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    
    if not arquivos:
        print("Nenhuma imagem encontrada!")
        return

    # Abre a primeira foto
    primeira_foto = os.path.join(PASTA_TEMP, arquivos[0])
    subprocess.Popen(f'start "" "{primeira_foto}"', shell=True)
    time.sleep(3.0) 

    for i in range(1, len(arquivos)):
        print(f"Foto {i+1}/{len(arquivos)}", end="\r")
        time.sleep(TEMPO_ESPERA)
        pyautogui.press('right')

    print("\n\nMissão Cumprida!")
    input("Pressione ENTER para limpar os ficheiros temporários...")
    shutil.rmtree(PASTA_TEMP)

if __name__ == "__main__":
    pyautogui.PAUSE = 0.0
    revisao_modo_insano()