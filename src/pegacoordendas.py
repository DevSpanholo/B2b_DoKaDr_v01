import pyautogui
import time
import keyboard

# Lista para armazenar as coordenadas memorizadas
saved_positions = []

print("Posicione o mouse nos cantos da área azul ou onde deseja salvar.")
print("Pressione a tecla 'm' para memorizar a posição.")
print("Pressione 'Ctrl+C' para encerrar e salvar as coordenadas.")

try:
    while True:
        # Verifica se a tecla 'm' foi pressionada
        if keyboard.is_pressed("m"):
            x, y = pyautogui.position()  # Captura a posição atual do mouse
            if (x, y) not in saved_positions:  # Evita salvar coordenadas duplicadas
                saved_positions.append((x, y))  # Adiciona a posição à lista
                print(f"Coordenadas salvas: ({x}, {y})")
            time.sleep(0.2)  # Pequeno intervalo para evitar múltiplos registros do mesmo clique

except KeyboardInterrupt:
    print("\nFinalizando e salvando coordenadas...")

    # Salva as coordenadas em um arquivo
    with open("saved_coordinates.txt", "w") as file:
        for pos in saved_positions:
            file.write(f"{pos}\n")

    print(f"Coordenadas salvas em 'saved_coordinates.txt'.")
