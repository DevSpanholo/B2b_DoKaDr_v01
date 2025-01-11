import pyautogui
import time
from pynput import keyboard

def configurar_coordenadas():
    """
    Configura as coordenadas interativamente para cima, direita, baixo e esquerda.
    O usuário deve posicionar o mouse e pressionar a tecla '=' para salvar cada direção.
    """
    print("Bem-vindo à configuração das coordenadas!")
    print("Posicione o mouse em cada direção (cima, direita, baixo, esquerda) e pressione '=' para salvar.")
    print("Pressione ESC a qualquer momento para cancelar.")

    direcoes = ["top", "right", "bottom", "left"]
    coordenadas = {}
    direcao_atual = 0

    def on_press(key):
        nonlocal direcao_atual

        try:
            if key.char == '=':  # Se a tecla '=' for pressionada
                # Captura a posição atual do mouse
                x, y = pyautogui.position()
                direcao = direcoes[direcao_atual]
                coordenadas[direcao] = (x, y)
                print(f"Coordenada para '{direcao}' salva: X={x}, Y={y}")

                # Avança para a próxima direção
                direcao_atual += 1

                if direcao_atual >= len(direcoes):
                    print("\nTodas as coordenadas foram configuradas com sucesso!")
                    print("Coordenadas finais:", coordenadas)
                    # Para o listener
                    return False
            elif key == keyboard.Key.esc:  # Se ESC for pressionado
                print("\nConfiguração cancelada pelo usuário.")
                return False

        except AttributeError:
            pass

    # Inicia o listener do teclado
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    # Salva as coordenadas em um arquivo (opcional)
    with open("coordenadas_direcoes.txt", "w") as arquivo:
        for direcao, coord in coordenadas.items():
            arquivo.write(f"{direcao}: {coord}\n")

    print("\nAs coordenadas foram salvas em 'coordenadas_direcoes.txt'.")
    return coordenadas

if __name__ == "__main__":
    coords = configurar_coordenadas()
    print("\nConfiguração concluída. Use estas coordenadas no seu código.")
    print(coords)
