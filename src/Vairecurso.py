import time
import pyautogui
from pathlib import Path


class ResourceManager:
    def __init__(self):
        self.resources_path = Path("recursos")
        self.resources_path.mkdir(exist_ok=True)  # Cria o diretório, se não existir
        self.map_region = None  # Região padrão: toda a tela

    def set_map_region(self, x, y, width, height):
        """Define a região do mapa onde os recursos serão buscados."""
        self.map_region = (x, y, width, height)
        print(f"Região do mapa definida para: {self.map_region}")

    def check_for_resource(self):
        """Verifica se há recursos para coletar na tela e coleta todos."""
        print("Procurando recursos na tela...")

        resources = ['1','2','3']
        resources_found = 0  # Contador de recursos encontrados

        for resource in resources:
            resource_path = self.resources_path / f"{resource}.png"
            if resource_path.exists():
                print(f"Procurando recurso: {resource} em {resource_path}")
                try:
                    # Procura todos os recursos na região definida
                    positions = list(pyautogui.locateAllOnScreen(
                        str(resource_path),
                        region=self.map_region,  # Limita a busca à região (se definida)
                        confidence=0.62  # Ajuste o nível de confiança
                    ))
                    if positions:
                        for position in positions:
                            position_center = pyautogui.center(position)
                            print(f"Recurso {resource} encontrado em {position_center}. Coletando...")
                            self.collect_resource(position_center)  # Realiza a coleta
                            resources_found += 1
                    else:
                        print(f"Recurso {resource} não encontrado na tela.")
                except Exception as e:
                    print(f"Erro ao procurar recurso {resource}: {e}")
            else:
                print(f"Arquivo de recurso {resource_path} não encontrado.")

        if resources_found > 0:
            print(f"Coleta concluída. Recursos coletados: {resources_found}")
            return True  # Indica que pelo menos um recurso foi coletado
        else:
            print("Nenhum recurso encontrado.")
            return False  # Nenhum recurso encontrado

    def collect_resource(self, position):
        """
        Realiza a coleta de um recurso na posição especificada.
        """
        print(f"Coletando recurso na posição {position}...")
        try:
            pyautogui.keyDown('shift')  # Pressiona a tecla Shift
            pyautogui.moveTo(position)  # Move o mouse para a posição do recurso
            time.sleep(0.2)  # Pequeno atraso para garantir precisão
            pyautogui.mouseDown()  # Pressiona o botão esquerdo
            pyautogui.mouseUp()  # Solta o botão esquerdo
            pyautogui.keyUp('shift')  # Libera a tecla Shift
            print("Recurso coletado com sucesso.")
        except Exception as e:
            print(f"Erro ao coletar recurso: {e}")
        finally:
            pyautogui.keyUp('shift')  # Garante que o Shift seja liberado em caso de erro

    def verify_region(self):
        """Verifica se a região foi definida corretamente (debug)."""
        if self.map_region:
            print(f"Região definida: {self.map_region}")
        else:
            print("Região não definida. A busca será realizada na tela inteira.")


if __name__ == "__main__":
    resource_manager = ResourceManager()

    # Defina a região do mapa e a área permitida
    resource_manager.set_map_region(0, 0, 1910, 1011)  # Exemplo: região do jogo

    # Verifica se a região foi definida corretamente
    resource_manager.verify_region()

    # Teste a busca e coleta de recursos
    resource_manager.check_for_resource()
