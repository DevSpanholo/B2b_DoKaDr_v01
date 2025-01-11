import sys
import pyautogui
import cv2
import numpy as np
import time
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyboardController

sys.path.append(r"D:\ultimo\src")

# Inicializa o controlador do mouse e teclado
mouse = Controller()
keyboard = KeyboardController()


time.sleep(5)  # Atraso para garantir que o jogo esteja em foco
# Função para verificar o inventário cheio
def verificar_inventario_cheio(template_path, confidencia=0.8):
    """Verifica se o inventário está cheio após abrir o inventário."""
    print("Garantindo que o jogo está em foco...")
    pyautogui.click(10, 10)  # Clique em uma área neutra para garantir foco no jogo
    time.sleep(0.5)

    print("Abrindo inventário com a tecla 'I'...")
    keyboard.press('i')
    time.sleep(0.3)  # Atraso para garantir o registro da tecla
    keyboard.release('i')
    time.sleep(2)  # Tempo para o inventário carregar completamente

    print("Capturando a tela para verificar o estado do inventário...")
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    print(f"Carregando o template: {template_path}")
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Erro: Não foi possível carregar o template {template_path}")
        return False

    resultado = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(resultado)

    inventario_cheio = max_val >= confidencia
    print(f"Inventário {'cheio' if inventario_cheio else 'não cheio'} (valor de correspondência: {max_val}).")

    print("Fechando inventário com a tecla 'ESC'...")
    keyboard.press(Key.esc)
    time.sleep(0.3)  # Pequeno atraso para simular um clique natural
    keyboard.release(Key.esc)
    time.sleep(0.5)

    return inventario_cheio




# Função para clicar em uma posição fixa
def clicar_posicao_fixa(pos_x, pos_y, tempo=0.2):
    """Realiza um clique em uma posição fixa."""
    mouse.position = (pos_x, pos_y)
    time.sleep(0.1)
    mouse.press(Button.left)
    time.sleep(tempo)
    mouse.release(Button.left)
    print(f"Clique realizado na posição ({pos_x}, {pos_y}).")


# Função para localizar uma imagem e clicar
def localizar_e_clicar(template_path, confidencia=0.8, tempo=2):
    """Localiza a imagem na tela e realiza o clique."""
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    if template is None:
        print(f"Erro: Não foi possível carregar o arquivo {template_path}")
        return

    resultado = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

    if max_val >= confidencia:
        pos_x, pos_y = max_loc
        pos_x += template.shape[1] // 2
        pos_y += template.shape[0] // 2
        mouse.position = (pos_x, pos_y)
        time.sleep(0.1)
        mouse.press(Button.left)
        time.sleep(0.1)
        mouse.release(Button.left)
        print(f"Elemento clicado em ({pos_x}, {pos_y}).")
        time.sleep(tempo)
    else:
        print("Elemento não encontrado.")


# Função para ir ao banco
def ir_ao_banco():
    """Executa as ações necessárias no banco."""
    print("Indo ao banco...")
    keyboard.press('h')  # Abre o mapa
    time.sleep(1)
    keyboard.release('h')
    time.sleep(2)

    #Passo 2: Clicar fora do portal
    print("Clicando fora do portal...")
    time.sleep(0.1)
    safe_x, safe_y = 315, 410  # Coordenadas do portal
    pyautogui.moveTo(safe_x, safe_y)
    pyautogui.click(button='left')
    print(" Clique fora do portal realizado")
    time.sleep(0.1)

    # Passo 3: Clicar no portal
    print("Clicando no portal...")
    time.sleep(0.1)
    portal_x, portal_y = 535, 420  # Coordenadas do portal
    pyautogui.moveTo(portal_x, portal_y)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()
    print(" Clique no portal realizado com sucesso.")

    # Passo 3: Digitar 'porkasso' e pressionar Enter
    print("Digitando 'ASTRUB'...")
    time.sleep(1)
    pyautogui.typewrite('astrub')

    print(" Clicando no portal...")
    confirma_x, confirma_y = 1235, 810  # Coordenadas do portal
    pyautogui.moveTo(confirma_x, confirma_y)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()
    print("Clique no portal realizado com sucesso - Iniciando rota.")

    # Passo 3: Caminhar para a esquerda
    time.sleep(5)
    pyautogui.moveTo(315, 410)  # Ajuste as coordenadas conforme necessário
    pyautogui.click()
    time.sleep(4)    

     # Passo 4: Executar ações do banco
    print("Executando ações do banco...")
    localizar_e_clicar(r"D:\ultimo\src\banco\bank.png", confidencia=0.5, tempo=2)
    time.sleep(5)
    localizar_e_clicar(r"D:\ultimo\src\banco\npc.png", confidencia=0.85, tempo=2)
    localizar_e_clicar(r"D:\ultimo\src\banco\consulta.png", confidencia=0.85, tempo=2)
    clicar_posicao_fixa(1214, 249, tempo=0.2)
    time.sleep(2)
    localizar_e_clicar(r"D:\ultimo\src\banco\transferir.png", confidencia=0.85, tempo=2)
    print("Ações do banco concluídas!")
    # Pressiona ESC para fechar o banco
    print("Fechando o banco...")
    keyboard.press(Key.esc)
    time.sleep(0.1)
    keyboard.release(Key.esc)
    print("Ações do banco concluídas!")

def retornar_para_rota():
    """Retorna ao ponto inicial após ações no banco."""

    # Função para retornar à rota
    print("Pressionando H...")
    keyboard.press('h')
    time.sleep(0.1)
    keyboard.release('h')

    print("Garantindo que o jogo está em foco...")
    pyautogui.click(10, 10)  # Clique em uma área neutra para garantir foco no jogo
    time.sleep(0.5)


    #Passo 1: Clicar fora do portal
    print("Clicando fora do portal...")
    time.sleep(0.1)
    safe_x, safe_y = 315, 410  # Coordenadas do portal
    pyautogui.moveTo(safe_x, safe_y)
    pyautogui.click(button='left')
    print(" Clique fora do portal realizado")
    time.sleep(0.1)


        

    # Passo 2: Clicar no portal
    print("Clicando no portal...")
    time.sleep(0.1)
    portal_x, portal_y = 535, 420  # Coordenadas do portal
    pyautogui.moveTo(portal_x, portal_y)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()
    print(" Clique no portal realizado com sucesso.")

    # Passo 3: Digitar 'porkasso' e pressionar Enter
    print("Digitando 'otom'...")
    time.sleep(1)
    pyautogui.typewrite('otom')

    print(" Clicando no portal...")
    confirma_x, confirma_y = 1235, 810  # Coordenadas do portal
    pyautogui.moveTo(confirma_x, confirma_y)
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()
    print("Clique no portal realizado com sucesso - Iniciando rota.")


# Ponto de entrada do módulo para teste
if __name__ == "__main__":
    template_path = r"D:\ultimo\src\banco\fullpods.png"
    if verificar_inventario_cheio(template_path):
        ir_ao_banco()
        retornar_para_rota()
    else:
        print("Inventário não está cheio. Continuando a rota normalmente.")
