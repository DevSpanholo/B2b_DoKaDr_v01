import os
import time
import pyautogui
from pathlib import Path
import keyboard  # Biblioteca alternativa para pressionamento de teclas

pyautogui.FAILSAFE = False  # Desabilita a função de segurança do PyAutoGUI

def test_saco_de_viagem():
    """
    Testa o fluxo do saco de viagem, incluindo:
    1. Garantir o foco da janela do jogo.
    2. Pressionar 'H' para abrir o menu do saco de viagem.
    3. Detectar a tela do saco de viagem.
    4. Clicar no portal.
    5. Digitar 'porkasso' e pressionar Enter.
    """
    print("[TEST] Iniciando teste do saco de viagem...")

    time.sleep(3)  # Aguarda 3 segundos antes de iniciar o teste
    # Caminho para a imagem
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script
    resources_path = Path(base_dir) / "recursos"
    sack_image_path = resources_path / "sacoviagem.png"

    print(f"[TEST] Verificando o caminho da imagem: {sack_image_path}")
    if not sack_image_path.exists():
        print(f"[TEST] ERRO: Imagem {sack_image_path} não encontrada.")
        return

    try:

        # Passo 2: Pressionar 'H'
        print("[TEST] Pressionando 'H' para abrir o menu do saco de viagem...")
        keyboard.press_and_release('h')  # Alternativa com biblioteca 'keyboard'
        time.sleep(3)  # Aguarda o menu carregar

        # Passo 3: Verificar se a tela do saco de viagem está visível
        print("[TEST] Procurando pela tela do saco de viagem...")
        sack_position = pyautogui.locateOnScreen(str(sack_image_path), confidence=0.8)

        if sack_position:
            print(f"[TEST] Tela do saco de viagem detectada em: {sack_position}.")
        else:
            print("[TEST] ERRO: Tela do saco de viagem não detectada.")
            return

        # Passo 4: Clicar no portal
        print("[TEST] Clicando no portal...")
        portal_x, portal_y = 535, 420  # Coordenadas do portal
        pyautogui.moveTo(portal_x, portal_y)
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.mouseUp()
        print("[TEST] Clique no portal realizado com sucesso.")

        # Passo 5: Digitar 'porkasso' e pressionar Enter
        print("[TEST] Digitando 'porkasso'...")
        time.sleep(1)
        pyautogui.typewrite('porkasso')

        # Passo 4: Clicar no portal
        print("[TEST] Clicando no portal...")
        confirma_x, confirma_y = 1235, 810  # Coordenadas do portal
        pyautogui.moveTo(confirma_x, confirma_y)
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.mouseUp()
        print("[TEST] Clique no portal realizado com sucesso.")
    except Exception as e:
        print(f"[TEST] ERRO durante o teste: {e}")

# Executa o teste
if __name__ == "__main__":
    test_saco_de_viagem()
