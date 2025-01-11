import keyboard
import json
import time

class RouteRecorder:
    def __init__(self, output_file="saved_route.json"):
        self.output_file = output_file
        self.route = []
        self.top_gather_count = 0  # Contador para "top" com "gather: True"

    def record_movement(self, direction):
        """Registra o movimento em uma direção, sempre com 'gather: True'."""
        movement = {"direction": direction, "gather": True}

        if direction == "top":
            self.top_gather_count += 1
            movement["annotation"] = f"# {self.top_gather_count}"

        self.route.append(movement)
        print(f"Movimento registrado: {movement}")

    def save_route(self):
        """Salva a rota em um arquivo JSON."""
        try:
            with open(self.output_file, "w") as file:
                json.dump(self.route, file, indent=4)
            print(f"Rota salva em {self.output_file}.")
        except Exception as e:
            print(f"Erro ao salvar a rota: {e}")

    def start_recording(self):
        """Inicia o processo de gravação de movimentos."""
        print("Pressione ´ para cima, ~ para baixo, ç para esquerda, ] para direita.")
        print("Pressione 's' para salvar a rota e sair.")

        try:
            while True:
                if keyboard.is_pressed("´"):  # Cima
                    self.record_movement("top")
                    time.sleep(0.2)  # Aguarda para evitar registros múltiplos
                elif keyboard.is_pressed("~"):  # Baixo
                    self.record_movement("bottom")
                    time.sleep(0.2)
                elif keyboard.is_pressed("ç"):  # Esquerda
                    self.record_movement("left")
                    time.sleep(0.2)
                elif keyboard.is_pressed("]"):  # Direita
                    self.record_movement("right")
                    time.sleep(0.2)
                elif keyboard.is_pressed("s"):  # Salvar e sair
                    print("Finalizando gravação...")
                    break
        except KeyboardInterrupt:
            print("Gravação interrompida manualmente.")

        self.save_route()


if __name__ == "__main__":
    output_path = "route.json"  # Nome do arquivo onde a rota será salva
    recorder = RouteRecorder(output_file=output_path)
    recorder.start_recording()
