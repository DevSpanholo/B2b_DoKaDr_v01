import time
from modules.screen import ScreenManager
from modules.resource import ResourceManager
from modules.movement import MovementManager
from modules.config import Config

class GameBot:
    def __init__(self):
        self.config = Config()
        self.screen = ScreenManager()
        self.resource = ResourceManager()
        self.movement = MovementManager(self.resource, self.screen)
    
    def run(self):
        """Executa o bot"""
        print("Iniciando bot de coleta...")
        self.movement.setup_positions()
        
        try:
            self.movement.follow_route()
        except KeyboardInterrupt:
            print("\nBot finalizado pelo usuário.")