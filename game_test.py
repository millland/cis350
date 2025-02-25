import sys
import coverage
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QPushButton, QWidget, QVBoxLayout, QStackedWidget, QComboBox)
from PyQt6.QtGui import QPixmap, QTransform
from PyQt6.QtCore import QTimer, Qt
from random import randint

# Board mappings for chutes and ladders
CHUTES_LADDERS = {
    1: 38,
    4: 14,
    9: 31,
    16: 6,
    28: 84,
    36: 44,
    40: 42,
    47: 26,
    49: 11,
    51: 67,
    56: 53,
    62: 19,
    64: 60,
    71: 91,
    80: 100,
    87: 24,
    93: 73,
    95: 75,
    98: 78
}


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
        pixmap = QPixmap("chuteslogo.webp")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(400, 200)

        # Buttons
        button_style = """
            QPushButton {
                font-size: 20px;
                padding: 12px;
                border-radius: 10px;
                background-color: green;
                color: white;
            }

        """

        select_players = QPushButton("Select Players")
        select_players.setStyleSheet(button_style)
        select_players.clicked.connect(self.start_game)

        load_button = QPushButton("Load Game")
        load_button.setStyleSheet(button_style)
        load_button.clicked.connect(self.load_game)

        quit_button = QPushButton("Quit")
        quit_button.setStyleSheet(button_style)
        quit_button.clicked.connect(sys.exit)

        # Add widgets to layout
        layout.addWidget(logo_label)
        layout.addWidget(select_players)
        layout.addWidget(load_button)
        layout.addWidget(quit_button)

        self.setLayout(layout)

    def start_game(self):
        self.stacked_widget.setCurrentIndex(1)  # Switch to players screen

    def load_game(self):
        print("Not yet implemented")


class PlayersScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Player selection dropdown
        self.player_select = QComboBox()
        self.player_select.addItems(["2 Players", "3 Players", "4 Players"])

        # Game Logo
        logo_label = QLabel(self)
        pixmap = QPixmap("chuteslogo.webp")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setScaledContents(True)
        logo_label.setFixedSize(400, 200)

        # Buttons
        button_style = """
            QPushButton {
                font-size: 20px;
                padding: 12px;
                border-radius: 10px;
                background-color: green;
                color: white;
            }

        """

        start_button = QPushButton("Start Game")
        start_button.setStyleSheet(button_style)
        start_button.clicked.connect(self.start_game)

        back_button = QPushButton("Back")
        back_button.setStyleSheet(button_style)
        back_button.clicked.connect(self.back)

        # Add widgets to layout
        layout.addWidget(logo_label)
        layout.addWidget(QLabel("Select Number of Players:"))
        layout.addWidget(self.player_select)
        layout.addWidget(start_button)
        layout.addWidget(back_button)

        # Set layout properly
        self.setLayout(layout)

    def start_game(self):
        num_players = int(self.player_select.currentText()[0])  # Extracts 2, 3, or 4
        self.stacked_widget.widget(2).set_num_players(num_players)  # Pass to MainGame
        self.stacked_widget.setCurrentIndex(2)  # Switch to game screen

    def back(self):
        self.stacked_widget.setCurrentIndex(0)  # Switch to start screen


class MainGame(QMainWindow, QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setWindowTitle("Chutes and Ladders")
        self.setGeometry(500, 250, 500, 900)
        self.stacked_widget = stacked_widget
        self.num_players = 2  # Default to 2 players
        self.player_pieces = []
        self.player_positions = [0] * 4  # Support for up to 4 players
        self.current_player = 0  # Track whose turn it is
        self.result = 0
        self.initUI()

    def set_num_players(self, num_players):
        self.num_players = num_players

    def initUI(self):
        # Background Image
        label1 = QLabel(self)
        label1.setGeometry(0, 0, 500, 500)
        pixmap = QPixmap("chutesandladders.jpg")
        label1.setPixmap(pixmap)
        label1.setScaledContents(True)

        # Assign pictures to players
        for i in range(self.num_players):
            piece = QLabel(self)
            pixmap = QPixmap(f"player{i + 1}.png")

            if pixmap.isNull():
                print(f"Error: player{i + 1}.png not found!")  # Debugging

            piece.setPixmap(pixmap)
            piece.setScaledContents(True)
            piece.setFixedSize(30, 30)  # size of icon
            x, y = self.get_pixel_position(1)  # Start at position 1
            piece.move(x, y)
            piece.raise_()  # Ensure the piece is drawn on top of the board
            self.player_pieces.append(piece)

        # Spinner Background (Rotated by 60°)
        self.spinner_bg_label = QLabel(self)
        self.spinner_bg_label.setGeometry(125, 550, 250, 250)

        self.spinner_bg_pixmap = QPixmap("spinner_transparent.png")  # Load original image
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
        self.spin_button.setGeometry(210, 545, 80, 40)
        self.spin_button.setStyleSheet(
            "font-size: 18px; "
            "font-weight: bold; "
            "color: white; "
            "background-color: blue; "
            "border-radius: 10px; "
            "padding: 10px; "
        )
        self.spin_button.clicked.connect(self.start_spin)

        # Result Label
        self.result_label = QLabel("Click 'Spin' to start", self)
        self.result_label.setGeometry(150, 510, 200, 30)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Turn Label
        self.turn_label = QLabel(self)
        self.turn_label.setGeometry(20, 550, 200, 30)
        self.turn_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turn_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_spinner)
        self.rotation_angle = 0
        self.target_rotation = 0  # Rotation stopping point

        # Quit Button
        self.quit = QPushButton("Quit", self)
        self.quit.setGeometry(420, 705, 70, 40)
        self.quit.setStyleSheet(
            "font-size: 15px; "
            "font-weight: bold; "
            "color: white; "
            "background-color: red; "
            "border-radius: 10px; "
            "padding: 10px; "
        )
        self.quit.clicked.connect(sys.exit)

        # Back Button
        self.back_button = QPushButton("Back", self)
        self.back_button.setGeometry(10, 705, 70, 40)
        self.back_button.setStyleSheet(
            "font-size: 15px; "
            "font-weight: bold; "
            "color: white; "
            "background-color: green; "
            "border-radius: 10px; "
            "padding: 10px; "
        )
        self.back_button.clicked.connect(self.back)

    def get_pixel_position(self, board_position):
        cell_size = 50  # Approximate cell size based on board dimensions
        start_x, start_y = 0, 450  # Bottom-left starting position

        # Mapping the board position (1-100) to pixel coordinates
        row = (board_position - 1) // 10  # Determine row (0-9)
        col = (board_position - 1) % 10  # Determine column (0-9)

        # If the row is even, move left to right
        if row % 2 == 0:
            x = col * cell_size
        else:  # If the row is odd, move right to left
            x = (9 - col) * cell_size

        y = start_y - (row * cell_size)  # Move up by row count

        return x, y

    def start_spin(self):
        self.spin_button.setEnabled(False)  # Disable button while spinning
        self.rotation_angle = 0
        self.target_rotation = 360 * randint(3, 5) + randint(0, 5) * 60  # Spin 3-5 times & land at a multiple of 60°
        self.timer.start(25)  # Rotate every 25ms

    def update_spinner(self):
        self.rotation_angle += 30  # Rotate by 30 degrees per frame
        if self.rotation_angle >= self.target_rotation:  # Stop at final angle
            self.timer.stop()
            self.show_result()
            self.spin_button.setEnabled(True)  # Re-enable button
        else:
            transform = QTransform().rotate(self.rotation_angle)
            rotated_pixmap = self.original_spinner_pixmap.transformed(transform,
                                                                      Qt.TransformationMode.SmoothTransformation)
            self.spinner_label.setPixmap(rotated_pixmap)

    def show_result(self):
        result = (self.target_rotation % 360) // 60 + 1  # Convert angle to a number 1-6
        self.result = result
        self.result_label.setText(f"You spun a {result}")

        QTimer.singleShot(500, self.next_turn)  # Wait half a second before moving the player

    def next_turn(self):
        # Move forward
        self.player_positions[self.current_player] += self.result
        new_position = self.player_positions[self.current_player]

        # Check for chutes or ladders and update position
        if new_position in CHUTES_LADDERS:
            new_position = CHUTES_LADDERS[new_position]

        # **Fix: Store the updated position**
        self.player_positions[self.current_player] = new_position

        # Move the player's piece on the board
        x, y = self.get_pixel_position(new_position)
        self.player_pieces[self.current_player].move(x, y)

        # Switch turn to next player
        self.current_player = (self.current_player + 1) % self.num_players
        self.turn_label.setText(f"Player {self.current_player + 1}'s Turn")

        self.result = 0
        self.spin_button.setEnabled(True)

    def back(self):
        self.stacked_widget.setCurrentIndex(1)  # Switch to player screen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Screens
        self.start_screen = StartScreen(self.stacked_widget)
        self.players_screen = PlayersScreen(self.stacked_widget)
        self.game_screen = MainGame(self.stacked_widget)

        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.start_screen)  # Index 0
        self.stacked_widget.addWidget(self.players_screen)  # Index 1
        self.stacked_widget.addWidget(self.game_screen)  # Index 2

        self.setWindowTitle("Chutes and Ladders")
        self.setGeometry(500, 250, 500, 800)


def main():
    print("Starting coverage...")
    cov = coverage.Coverage()
    cov.start()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    try:
        app.exec()
    finally:
        print("Stopping coverage...")
        cov.stop()
        cov.save()
        cov.report()
        print("Coverage report saved.")


if __name__ == "__main__":
    main()
