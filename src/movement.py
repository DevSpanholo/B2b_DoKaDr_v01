import time
import keyboard
import pyautogui
from pathlib import Path
from Vairecurso import ResourceManager
from screen import ScreenManager
from Vaibanco import verificar_inventario_cheio, ir_ao_banco, retornar_para_rota
from Entroubatalha import BattleManager  

pyautogui.FAILSAFE = False  # Desabilita a função de segurança do PyAutoGUI


class MovementManager:
    def __init__(self):
        self.resource_manager = ResourceManager() 
        self.screen_manager = ScreenManager()  
        self.battle_manager = BattleManager()  

        # Define a rota
        self.route =  [
            #-46,18
            {'direction': 'bottom'},
            #-46,19
            {'direction': 'left'},
            #-47,19
            {'direction': 'left'},
            #-48,19
            {'direction': 'left'},
            #-49,19
            {'direction': 'left'},
            #-50,19
            {'direction': 'bottom'},
            #-50,20
            {'direction': 'bottom'},
            #-50,21
            {'direction': 'left'},
            #-51,21
            {'direction': 'top'},
            #-51,20
            {'direction': 'left','gather': True},
            #-52,20
            {'direction': 'top','gather': True},
            #-52,19
            {'direction': 'right'},
            #-51,19
            {'direction': 'top','gather': True},
            #-51,18
            {'direction': 'top','gather': True},
            #-51,17
            {'direction': 'top'},
            #-51,16
            {'direction': 'left','gather': True},
            #-52,16
            {'direction': 'top','gather': True},
            #-52,15
            {'direction': 'left','gather': True},
            #-53,15
            {'direction': 'left','gather': True},
            #-54,15
            {'direction': 'left','gather': True},
            #-55,15
            {'direction': 'left'},
            #-56,15
            {'direction': 'top','gather': True},
            #-56,14
            {'direction': 'top'},
            #-56,13
            {'direction': 'right','gather': True},
            #-55,13
            {'direction': 'top'},
            #-55,12
            {'direction': 'top'},
            #-55,11
            {'direction': 'top'},
            #-55,10
            {'direction': 'right','gather': True},
            #54,10
            {'direction': 'bottom'},
            #-54,11
            {'direction': 'right','gather': True},
            #-53,11
            {'direction': 'right',},
            #-52,11
            {'direction': 'bottom','gather': True},
            #-52,12
            {'direction': 'left','gather': True},
            #-53,12
            {'direction': 'bottom','gather': True},
            #-53,13
            {'direction': 'right',},
            #-52,13
            {'direction': 'right','gather': True},
            #-51,13
            {'direction': 'top','gather': True},
            #-51,12
            {'direction': 'right'},
            #-50,12
            {'direction': 'right'},
            #-49,12
            {'direction': 'right'},
            #-48,12
            {'direction': 'right'},
            #-47,12
            {'direction': 'bottom'},
            #-47,13
            {'direction': 'bottom'},
            #-47,14
            {'direction': 'bottom'},
            #-47,15
            {'direction': 'bottom'}, 
            #-47,16
            {'direction': 'right'}, 
            #-46,16
            {'direction': 'bottom'}, 
            #46,17
            {'direction': 'bottom'}, 
            ]

    def move_to_direction(self, direction):
        """Move o personagem para a direção especificada."""
        directions = {
            "top": (1089, 25),
            "bottom": (1298, 907),
            "left": (276, 529),
            "right": (1746, 290),
        }

        if direction not in directions:
            print(f"Direção inválida: {direction}")
            return False

        x, y = directions[direction]
        print(f"Movendo para: {direction} nas coordenadas ({x}, {y})...")

        try:
            keyboard.press("shift")
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            time.sleep(1)
            pyautogui.mouseUp()
            keyboard.release("shift")
            print(f"Movimento para '{direction}' concluído.")
            return True
        except Exception as e:
            print(f"Erro ao mover para {direction}: {e}")
            pyautogui.keyUp("shift")  # Garante que o Shift seja liberado em caso de erro
            return False

    def follow_route(self, template_path, num_loops=1500):
        """Segue a rota definida e realiza ações de inventário e coleta."""
        print(f"Executando rota {num_loops} vez(es)...")

        for loop in range(1, num_loops + 10):
            print(f"\nIniciando volta {loop} de {num_loops}...")

            # Atraso inicial para garantir que o mapa carregue completamente
            print("Aguardando o carregamento inicial do mapa...")
            time.sleep(3)

            for i, step in enumerate(self.route):
                if keyboard.is_pressed("-"):  # Verifica se a tecla '-' foi pressionada
                    print("Script interrompido pelo usuário.")
                    return  # Sai da função

                # Verifica batalha no início de cada passo
                print("Verificando se o personagem está em batalha...")
                if self.battle_manager.is_in_battle():
                    print("Personagem está em batalha. Tentando abandonar...")
                    if self.battle_manager.abandon_battle():
                        print("Batalha abandonada com sucesso. Reiniciando a rota.")
                        return self.follow_route(template_path, num_loops)  # Reinicia a rota

                direction = step["direction"]
                gather = step.get("gather", False)

                print(f"Movendo para: {direction} (Passo {i + 1} da rota)")
                try:
                    if self.move_to_direction(direction):
                        print("Aguardando mudança de mapa...")
                        self.screen_manager.wait_map_change()
                        time.sleep(1)  # Pequeno delay após a mudança de mapa

                        if gather:
                            print(f"Verificando recursos no passo {i + 1}...")
                            resource_found = self.resource_manager.check_for_resource()
                            if resource_found:
                                print("Recurso coletado com sucesso. Aguardando próximo movimento.")
                                time.sleep(1)  # Pequeno delay após coleta

                                # Verifica batalha após a coleta
                                print("Verificando batalha após coleta de recurso...")
                                time.sleep(4)  # Espera 4 segundos para garantir
                                if self.battle_manager.is_in_battle():
                                    print("Personagem entrou em batalha após coleta. Tentando abandonar...")
                                    if self.battle_manager.abandon_battle():
                                        print("Batalha abandonada com sucesso. Reiniciando a rota.")
                                        return self.follow_route(template_path, num_loops)  # Reinicia a rota
                            else:
                                print("Nenhum recurso encontrado neste mapa.")
                except Exception as e:
                    print(f"Erro durante o passo {i + 1}: {e}. Continuando para o próximo passo.")

            # Verificar o inventário somente no final de cada loop completo da rota
            print("Verificando inventário após completar a volta...")
            try:
                inventario_cheio = verificar_inventario_cheio(template_path)
                if inventario_cheio:
                    print("Inventário cheio detectado. Indo ao banco...")
                    ir_ao_banco()
                    retornar_para_rota()
                    print("Retornando à posição inicial e reiniciando a rota.")
                    return self.follow_route(template_path, num_loops)
            except Exception as e:
                print(f"Erro ao verificar inventário: {e}. Continuando a rota...")

            print(f"Volta {loop} concluída!")

        print("\nTodas as voltas concluídas. Rota finalizada.")




# Exemplo de uso
if __name__ == "__main__":
    template_path = r"D:\ultimo\src\banco\fullpods.png"
    movement_manager = MovementManager()
    movement_manager.follow_route(template_path)
