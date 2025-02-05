import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QPushButton, QWidget, QVBoxLayout, QStackedWidget)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from random import randint


class StartScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Game Logo
        logo_label = QLabel(self)
        pixmap = QPixmap("chuteslogo.webp")  # Use an actual logo file
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(400, 250)  # Adjust size

        # Buttons
        start_button = QPushButton("Start Game")
        start_button.setStyleSheet("font-size: 20px; padding: 10px;")
        start_button.clicked.connect(self.start_game)

        load_button = QPushButton("Load Game")
        load_button.setStyleSheet("font-size: 20px; padding: 10px;")
        load_button.clicked.connect(self.load_game)

        quit_button = QPushButton("Quit")
        quit_button.setStyleSheet("font-size: 20px; padding: 10px;")
        quit_button.clicked.connect(sys.exit)

        # Add widgets to layout
        layout.addWidget(logo_label)
        layout.addWidget(start_button)
        layout.addWidget(load_button)
        layout.addWidget(quit_button)

        self.setLayout(layout)

    def start_game(self):
        self.stacked_widget.setCurrentIndex(1)  # Switch to game screen

    def load_game(self):
        print("Not yet implemented")


class MainGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chutes and Ladders")
        self.setGeometry(500, 250, 500, 600)
        self.initUI()

        # Background Image
        label1 = QLabel(self)
        label1.setGeometry(0, 0, 500, 500)
        pixmap = QPixmap("chutesandladders.jpg")
        label1.setPixmap(pixmap)
        label1.setScaledContents(True)

        # Label for dice roll result
        self.roll_label = QLabel("Click 'Roll Dice' to start", self)
        self.roll_label.setGeometry(150, 550, 200, 30)
        self.roll_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.roll_label.setStyleSheet("font-size: 18px; font-weight: bold;")

    def roll_dice(self):
        dice = randint(1, 6)
        self.roll_label.setText(f"You rolled a {dice}")  # Update label text

    def initUI(self):
        roll = QPushButton('Roll Dice', self)
        roll.setGeometry(175, 500, 150, 50)
        roll.setStyleSheet("font-size: 25px;")
        roll.clicked.connect(self.roll_dice)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Screens
        self.start_screen = StartScreen(self.stacked_widget)
        self.game_screen = MainGame()

        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.start_screen)  # Index 0
        self.stacked_widget.addWidget(self.game_screen)   # Index 1

        self.setWindowTitle("Chutes and Ladders")
        self.setGeometry(500, 250, 500, 600)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
