from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QTextEdit, QProgressBar
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import hashlib
from movement import MovementManager
import keyboard  # Para atribuir atalhos de interrupção


class BotWorker(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, bot_manager, parent=None):
        super().__init__(parent)
        self.bot_manager = bot_manager
        self.running = True  # Controle para parar o bot

    def run(self):
        try:
            while self.running:  # Loop infinito até ser parado
                total_steps = len(self.bot_manager.route)
                for i, step in enumerate(self.bot_manager.route):
                    if not self.running:  # Verifica se o bot foi parado
                        self.log_signal.emit("⏹️ Stop Bot.")
                        return

                    if keyboard.is_pressed('-'):  # Tecla de parada
                        self.log_signal.emit("⏹️ Bot stop using '-'!")
                        self.running = False
                        return

                    # Move o bot para a direção especificada
                    direction = step["direction"]
                    gather = step.get("gather", False)
                    self.log_signal.emit(f"Movendo para: {direction} (Recurso: {gather})")
                    success = self.bot_manager.move_to_direction(direction)

                    if success:
                        self.log_signal.emit("Awaiting map change...")
                        self.bot_manager.screen_manager.wait_map_change()
                        self.sleep_with_interrupt(1)

                        if gather:
                            self.log_signal.emit("Verify resource...")
                            resource_found = self.bot_manager.resource_manager.check_for_resource()
                            if resource_found:
                                self.log_signal.emit("✅ Nice resource found!") 
                            else:
                                self.log_signal.emit("❌ Piu! Piu! Ressource not found!")
                            self.sleep_with_interrupt(2)

                        # Atualiza progresso
                        progress = int((i + 1) / total_steps * 100)
                        self.progress_signal.emit(progress)

                    self.log_signal.emit("Awaiting new move...")
                    self.sleep_with_interrupt(2)

                self.log_signal.emit("🔄 End of route. Restarting...")
                self.progress_signal.emit(0)  # Reseta a barra de progresso
        except Exception as e:
            self.error_signal.emit(f"❌ Erro: {e}")
        finally:
            self.finished_signal.emit()

    def monitor_keyboard(self):
        """
        Monitora a tecla '-' globalmente para interromper o bot.
        """
        keyboard.wait('-')  # Aguarda a tecla '-' ser pressionada
        self.running = False
        self.log_signal.emit("⏹️ Bot stop using '-'!")

    def sleep_with_interrupt(self, seconds):
        """Aguarda por 'seconds' segundos com verificação de interrupção."""
        for _ in range(seconds * 10):
            if not self.running:
                break
            self.msleep(100)

    def stop(self):
        self.running = False



class BotInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clarck Bot")
        self.setGeometry(70, 70, 150, 100)
        self.setStyleSheet("background-color: #f5f5f5;")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Sempre no topo
        self.init_ui()

        self.bot_manager = MovementManager()  # Inicializa o gerenciador do bot
        self.bot_worker = None  # A thread do bot será inicializada aqui
        self.is_activated = False  # Controle do estado de ativação

    def init_ui(self):
        container = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Título
        title_label = QLabel("Clarck Bot")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Campo para chave de ativação
        key_layout = QVBoxLayout()
        key_label = QLabel("Key activation:")
        key_label.setStyleSheet("font-size: 16px; color: #555;")
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Digit your activation key")
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.setStyleSheet(
            "padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;"
        )
        key_layout.addWidget(key_label)
        key_layout.addWidget(self.key_input)

        # Botão de Ativação
        self.activate_button = QPushButton("Active!")
        self.activate_button.setStyleSheet(
            "background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;"
            "font-size: 14px; font-weight: bold;"
        )
        self.activate_button.clicked.connect(self.activate_bot)
        key_layout.addWidget(self.activate_button)
        layout.addLayout(key_layout)

        # Log de Status
        log_label = QLabel("Logs:")
        log_label.setStyleSheet("font-size: 16px; color: #555;")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet(
            "padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;"
            "background-color: #fff;"
        )
        layout.addWidget(log_label)
        layout.addWidget(self.log_output)

        # Barra de Progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Botões de Controle
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Bot")
        self.start_button.setStyleSheet(
            "background-color: #008CBA; color: white; padding: 10px; border-radius: 5px;"
            "font-size: 14px; font-weight: bold;"
        )
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.start_bot)

        self.stop_button = QPushButton("Stop Bot")
        self.stop_button.setStyleSheet(
            "background-color: #f44336; color: white; padding: 10px; border-radius: 5px;"
            "font-size: 14px; font-weight: bold;"
        )
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_bot)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def validate_key(self, key):
        secret = "minha-chave-secreta"
        try:
            key_parts = key.split("-")
            if len(key_parts) != 2:
                return False
            key_body, key_hash = key_parts
            expected_hash = hashlib.sha256((key_body + secret).encode()).hexdigest()[:8]
            return key_hash == expected_hash
        except Exception:
            return False

    def activate_bot(self):
        key = self.key_input.text()
        if self.validate_key(key):
            self.update_log("✅ Initial key validated. Bot activated.")
            self.is_activated = True
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(True)
        else:
            self.update_log("❌ Invalid key. Please, try again.")

    def start_bot(self):
        if not self.is_activated:
            self.update_log("⚠️ Bot not activated. Please, enter a valid key.")
            return

        self.update_log("▶️ Bot started.")
        self.bot_worker = BotWorker(self.bot_manager)
        self.bot_worker.log_signal.connect(self.update_log)
        self.bot_worker.progress_signal.connect(self.update_progress)
        self.bot_worker.finished_signal.connect(self.bot_finished)
        self.bot_worker.error_signal.connect(self.update_log)
        self.bot_worker.start()

    def stop_bot(self):
        if self.bot_worker:
            self.bot_worker.stop()

    def bot_finished(self):
        self.update_log("✅ Bot finished.")
        self.progress_bar.setValue(100)

    def update_log(self, message):
        self.log_output.append(message)

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BotInterface()
    window.show()
    sys.exit(app.exec_())
