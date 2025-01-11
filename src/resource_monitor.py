import pytesseract
from PIL import Image, ImageEnhance, ImageOps
import pyautogui
import time
import os

class ResourceMonitor:
    def __init__(self, tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

        # Slots com coordenadas (ajuste com precisão)
        self.slots = {
            1: (639, 980, 36, 36),
            2: (681, 981, 39, 34),
            3: (725, 979, 38, 35),
        }
        self.last_counts = {slot: 0 for slot in self.slots}

        # Pasta para salvar imagens de debug
        self.debug_folder = "debug_images"
        os.makedirs(self.debug_folder, exist_ok=True)

    def capture_region(self, region):
        """Captura uma região específica da tela."""
        screenshot = pyautogui.screenshot(region=region)
        return screenshot

    def preprocess_image(self, image, slot):
        """Processa a imagem para melhorar a leitura OCR."""
        # Converte para escala de cinza
        image = image.convert("L")
        # Aumenta o contraste
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(3)  # Ajuste de contraste
        # Redimensiona a imagem (aumenta o tamanho)
        image = image.resize((image.width * 3, image.height * 3), Image.LANCZOS)
        # Binariza a imagem (ajuste fino)
        image = ImageOps.autocontrast(image)

        # Salva a imagem processada para debug
        debug_path = os.path.join(self.debug_folder, f"slot_{slot}.png")
        image.save(debug_path)

        return image

    def extract_number(self, image, slot):
        """Extrai o número da imagem usando OCR."""
        processed_image = self.preprocess_image(image, slot)
        text = pytesseract.image_to_string(processed_image, config="--psm 6 digits")
        numbers = [int(num) for num in text.split() if num.isdigit()]
        return numbers[0] if numbers else 0

    def monitor_resources(self, duration=60):
        start_time = time.time()
        while time.time() - start_time < duration:
            for slot, region in self.slots.items():
                image = self.capture_region(region)
                count = self.extract_number(image, slot)

                if count != self.last_counts[slot]:
                    print(f"Slot {slot}: {count} coletado")
                    self.last_counts[slot] = count
            time.sleep(1)

if __name__ == "__main__":
    tesseract_path = r"C:\Tesseract-OCR\tesseract.exe"  # Caminho do Tesseract OCR
    monitor = ResourceMonitor(tesseract_path)
    print("Iniciando monitoramento dos slots...")
    monitor.monitor_resources(duration=60)
