import time
import numpy as np
import pyautogui


class ScreenManager:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.region = (
            0, 0, self.screen_width, self.screen_height  # Região: Tela inteira
        )

    def is_screen_dark(self, screenshot):
        """
        Verifica se a tela está escura com base no brilho médio e contraste.
        """
        img_array = np.array(screenshot.convert("L"))  # Converte para escala de cinza
        average_brightness = np.mean(img_array)
        dark_pixels_ratio = np.sum(img_array < 50) / img_array.size
        print(f"Brilho médio: {average_brightness}, Proporção escura: {dark_pixels_ratio}")
        return average_brightness < 70 or dark_pixels_ratio > 0.5

    def has_significant_change(self, screenshot1, screenshot2, threshold=0.1):
        """
        Compara duas capturas de tela para detectar mudanças significativas.
        """
        img1 = np.array(screenshot1.convert("L"))
        img2 = np.array(screenshot2.convert("L"))
        diff = np.abs(img1.astype("int16") - img2.astype("int16"))
        diff_ratio = np.sum(diff > 30) / img1.size
        print(f"Proporção de mudança entre quadros: {diff_ratio}")
        return diff_ratio > threshold

    def wait_map_change(self):
        """
        Aguarda uma mudança de mapa com base na detecção de tela escura e clara.
        """
        print("Aguardando mudança de mapa...")

        prev_screenshot = pyautogui.screenshot(region=self.region)

        # Detecta escurecimento da tela
        def detect_dark():
            current_screenshot = pyautogui.screenshot(region=self.region)
            if self.is_screen_dark(current_screenshot):
                return True
            return self.has_significant_change(prev_screenshot, current_screenshot)

        if not self.wait_until(detect_dark, timeout=10):
            print("Erro: Escurecimento da tela não detectado.")
            return

        print("Tela escurecida. Aguardando clareamento...")

        # Detecta clareamento da tela
        def detect_light():
            current_screenshot = pyautogui.screenshot(region=self.region)
            return not self.is_screen_dark(current_screenshot)

        if not self.wait_until(detect_light, timeout=10):
            print("Erro: Clareamento da tela não detectado.")
            return

        print("Mudança de mapa detectada!")

    def wait_until(self, condition, timeout=4, interval=0.1):
        """
        Aguarda até que a condição seja verdadeira ou o tempo limite seja atingido.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if condition():
                return True
            time.sleep(interval)
        return False


if __name__ == "__main__":
    screen_manager = ScreenManager()

    # Aguarda a mudança de mapa
    screen_manager.wait_map_change()
