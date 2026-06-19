import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import QTimer, Qt
class SimonCuadrado(QWidget):
    def __init__(self):
        super().__init__()
        self.colors_config = {
            "yellow": {"off": "#8B8000", "on": "#FFFF00"},
            "blue":   {"off": "#00008B", "on": "#0000FF"},
            "red":    {"off": "#8B0000", "on": "#FF0000"},
            "green":  {"off": "#006400", "on": "#00FF00"}
        }
        self.sequence = []
        self.user_sequence = []
        self.is_playback = False
        self.playback_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.play_next_color)
        self.off_timer = QTimer()
        self.off_timer.setSingleShot(True)
        self.off_timer.timeout.connect(self.turn_off_all_buttons)
        self.init_ui()
    def init_ui(self):
        self.setWindowTitle("Simon")
        self.setStyleSheet("background-color: #1A1A1A;")
        layout = QGridLayout()
        layout.setSpacing(15)
        self.setLayout(layout)
        self.buttons = {
            "yellow": QPushButton(self),
            "blue":   QPushButton(self),
            "red":    QPushButton(self),
            "green":  QPushButton(self)
        }
        for color, btn in self.buttons.items():
            btn.setFixedSize(200, 200)
            btn.clicked.connect(lambda checked, c=color: self.handle_user_click(c))
            self.set_button_style(color, state="off")
        layout.addWidget(self.buttons["yellow"], 0, 0)
        layout.addWidget(self.buttons["blue"], 0, 1)
        layout.addWidget(self.buttons["red"], 1, 0)
        layout.addWidget(self.buttons["green"], 1, 1)
        self.btn_center = QPushButton("START", self)
        self.btn_center.setFixedSize(120, 50)
        self.btn_center.clicked.connect(self.start_game)
        self.btn_center.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #FFFFFF;
                border: 2px solid #555555;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #444444; }
            QPushButton:disabled { background-color: #222222; color: #888888; }
        """)
        layout.addWidget(self.btn_center, 0, 0, 2, 2, alignment=Qt.AlignCenter)
        self.setFixedSize(self.hintChangedSize())
    def hintChangedSize(self):
        return self.layout().minimumSize()
    def set_button_style(self, color, state="off"):
        """Cambia el color de fondo usando CSS plano de PyQt5"""
        hex_color = self.colors_config[color][state]
        self.buttons[color].setStyleSheet(f"""
            QPushButton {{
                background-color: {hex_color};
                border: none;
            }}
        """)
    def start_game(self):
        self.sequence = []
        self.btn_center.setEnabled(False)
        self.next_turn()
    def next_turn(self):
        self.user_sequence = []
        self.sequence.append(random.choice(["yellow", "blue", "red", "green"]))
        self.btn_center.setText(f"SCORE: {len(self.sequence) - 1}")
        self.start_playback()
    def start_playback(self):
        self.is_playback = True
        self.playback_index = 0
        for btn in self.buttons.values():
            btn.setEnabled(False)
        self.timer.start(800) 
    def play_next_color(self):
        if self.playback_index < len(self.sequence):
            color = self.sequence[self.playback_index]
            self.set_button_style(color, state="on")
            self.off_timer.start(500)
            self.playback_index += 1
        else:
            self.timer.stop()
            self.is_playback = False
            for btn in self.buttons.values():
                btn.setEnabled(True)
    def turn_off_all_buttons(self):
        for color in self.buttons.keys():
            self.set_button_style(color, state="off")
    def handle_user_click(self, color):
        if self.is_playback:
            return
        self.set_button_style(color, state="on")
        QTimer.singleShot(200, lambda: self.set_button_style(color, state="off"))
        self.user_sequence.append(color)
        current_step = len(self.user_sequence) - 1
        if self.user_sequence[current_step] != self.sequence[current_step]:
            self.game_over()
            return
        if len(self.user_sequence) == len(self.sequence):
            for btn in self.buttons.values():
                btn.setEnabled(False)
            QTimer.singleShot(1000, self.next_turn)
    def game_over(self):
        self.btn_center.setText("RETRY")
        self.btn_center.setEnabled(True)
        for btn in self.buttons.values():
            btn.setEnabled(False)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = SimonCuadrado()
    game.show()
    sys.exit(app.exec_())
