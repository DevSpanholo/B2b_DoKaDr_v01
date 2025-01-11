import pyautogui
import time
from pathlib import Path
from pynput.keyboard import Controller, Key

class BattleManager:
    def __init__(self):
        # Inicializa o caminho para as imagens de batalha
        self.battle_images_path = Path("batalha")
        if not self.battle_images_path.exists():
            self.battle_images_path.mkdir()  # Cria o diretório se ele não existir

        # Mapeamento dos botões para as imagens
        self.buttons = {
            "sair": str(self.battle_images_path / "sair.png"),  # Botão "sair" da batalha
        }

        # Inicializa o controlador do teclado
        self.keyboard = Controller()

    def is_in_battle(self):
        """Verifica se o personagem está em batalha."""
        print("Verificando se o personagem está em batalha...")
        for button_name, button_path in self.buttons.items():
            if Path(button_path).exists():
                try:
                    position = pyautogui.locateCenterOnScreen(button_path, confidence=0.7)
                    if position:
                        print(f"Botão '{button_name}' detectado na posição {position}.")
                        return True
                except pyautogui.ImageNotFoundException:
                    print(f"Botão '{button_name}' não encontrado na tela.")
            else:
                print(f"Imagem do botão '{button_name}' não encontrada no diretório: {button_path}.")
        print("Nenhum botão de batalha detectado.")
        return False

    def abandon_battle(self):
        """Tenta abandonar a batalha clicando no botão 'sair', pressionando Enter e depois ESC."""
        button_path = self.buttons.get("sair")
        if Path(button_path).exists():
            try:
                position = pyautogui.locateCenterOnScreen(button_path, confidence=0.7)
                if position:
                    print(f"Clicando no botão 'sair' na posição {position}...")
                    pyautogui.moveTo(position)
                    pyautogui.click()
                    time.sleep(2)  # Pequeno atraso para garantir o clique

                    # Pressiona Enter para confirmar a saída
                    print("Pressionando Enter para confirmar a saída...")
                    self.keyboard.press(Key.enter)
                    time.sleep(0.1)
                    self.keyboard.release(Key.enter)
                    time.sleep(2)  # Pequeno atraso após confirmar

                    # Pressiona ESC para fechar o menu restante
                    print("Pressionando ESC para fechar o menu...")
                    self.keyboard.press(Key.esc)
                    time.sleep(0.1)
                    self.keyboard.release(Key.esc)
                    time.sleep(0.5)  # Pequeno atraso para garantir que o menu foi fechado
                    return True
            except pyautogui.ImageNotFoundException:
                print("Botão 'sair' não encontrado durante a tentativa de abandono.")
        else:
            print("Imagem do botão 'sair' não encontrada para abandono.")
        print("Nenhum botão de saída encontrado para abandonar a batalha.")
        return False
