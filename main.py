import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QPushButton, QWidget, QVBoxLayout, QStackedWidget)
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtCore import QTimer, Qt
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

    def initUI(self):
        # Background Image
        label1 = QLabel(self)
        label1.setGeometry(0, 0, 500, 500)
        pixmap = QPixmap("chutesandladders.jpg")
        label1.setPixmap(pixmap)
        label1.setScaledContents(True)

        # Background Image
        label1 = QLabel(self)
        label1.setGeometry(0, 0, 500, 500)
        pixmap = QPixmap("chutesandladders.jpg")
        label1.setPixmap(pixmap)
        label1.setScaledContents(True)

        # Spinner Background (Rotated by 60°)
        self.spinner_bg_label = QLabel(self)
        self.spinner_bg_label.setGeometry(125, 550, 250, 250)


        self.spinner_bg_pixmap = QPixmap("spinner.jpeg")  # Load original image
        transform = QTransform().rotate(-120)  # Rotate counterclockwise by 60°
        rotated_bg_pixmap = self.spinner_bg_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)

        self.spinner_bg_label.setPixmap(rotated_bg_pixmap)
        self.spinner_bg_label.setScaledContents(True)

        # Spinner Arrow (Rotating)
        self.spinner_label = QLabel(self)
        self.spinner_label.setGeometry(175, 600, 150, 150)
        self.spinner_pixmap = QPixmap("curvy-arrow.png")  # Replace with actual arrow image
        self.original_spinner_pixmap = self.spinner_pixmap  # Keep original for rotation
        self.spinner_label.setPixmap(self.spinner_pixmap)
        self.spinner_label.setScaledContents(True)
        self.spinner_label.setFixedSize(150, 150)
        self.spinner_label.setStyleSheet("background: transparent;")
        self.spinner_label.raise_()


        # Spin Button
        self.spin_button = QPushButton("Spin", self)
        self.spin_button.setGeometry(210, 550, 80, 40)
        self.spin_button.setStyleSheet("font-size: 20px;")
        self.spin_button.clicked.connect(self.start_spin)

        # Result Label
        self.result_label = QLabel("Click 'Spin' to start", self)
        self.result_label.setGeometry(150, 520, 200, 30)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_spinner)
        self.rotation_angle = 0
        self.target_rotation = 0  # Rotation stopping point

        # Quit Button
        self.quit = QPushButton("Quit", self)
        self.quit.setGeometry(420, 705, 70, 40)
        self.quit.setStyleSheet("font-size: 15px;")
        self.quit.clicked.connect(sys.exit)

    def start_spin(self):
        self.spin_button.setEnabled(False)  # Disable button while spinning
        self.rotation_angle = 0
        self.target_rotation = 360 * randint(3, 5) + randint(0, 5) * 60  # Spin 3-5 times & land at a multiple of 60°
        self.timer.start(50)  # Rotate every 50ms

    def update_spinner(self):
        self.rotation_angle += 30  # Rotate by 30 degrees per frame
        if self.rotation_angle >= self.target_rotation:  # Stop at final angle
            self.timer.stop()
            self.show_result()
            self.spin_button.setEnabled(True)  # Re-enable button
        else:
            transform = QTransform().rotate(self.rotation_angle)
            rotated_pixmap = self.original_spinner_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
            self.spinner_label.setPixmap(rotated_pixmap)

    def show_result(self):
        result = (self.target_rotation % 360) // 60 + 1  # Convert angle to a number 1-6
        self.result_label.setText(f"You spun a {result}")


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
        self.setGeometry(500, 250, 500, 900)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
