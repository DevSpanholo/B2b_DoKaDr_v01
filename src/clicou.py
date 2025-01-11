import pyautogui
import time

def obter_coordenadas():
    """
    Captura e exibe as coordenadas do mouse em tempo real.
    Armazena as coordenadas quando o botão esquerdo é clicado.
    """
    print("Movimente o mouse para ver as coordenadas. Clique com o botão esquerdo para armazenar.")
    print("Pressione CTRL+C para encerrar.")
    coordenadas = []

    try:
        while True:
            # Obtém a posição atual do mouse
            x, y = pyautogui.position()
            print(f"\rPosição atual do mouse: X={x}, Y={y}", end='')

            
            time.sleep(0.1)  # Reduz a frequência de leitura
    except KeyboardInterrupt:
        print("\nArmazenando coordenadas...")
if __name__ == "__main__":
    obter_coordenadas()
