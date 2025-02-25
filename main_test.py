import sys
import unittest
from random import randint

from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt, QTimer

from main import MainWindow, MainGame, PlayersScreen, StartScreen, CHUTES_LADDERS

# Create QApplication instance for tests
app = QApplication(sys.argv)


class TestStartScreen(unittest.TestCase):
    def setUp(self):
        # Create instance of main window for testing
        self.window = MainWindow()
        self.start_screen = self.window.start_screen
        self.stacked_widget = self.window.stacked_widget

    def test_screen_switch(self):
        # Simulate clicking the "Select Players" button on the start screen.
        select_buttons = self.start_screen.findChildren(type(self.start_screen))
        # Alternatively, we call the method directly.
        self.start_screen.start_game()
        self.assertEqual(self.stacked_widget.currentIndex(), 1)


class TestPlayersScreen(unittest.TestCase):
    def setUp(self):
        self.window = MainWindow()
        self.players_screen = self.window.players_screen
        self.stacked_widget = self.window.stacked_widget
        self.game_screen = self.window.game_screen

    def test_num_players(self):
        # test if the game correctly sets the number of players
        # using 3 players for this test
        self.players_screen.player_select.setCurrentText("3 Players")
        self.players_screen.start_game()
        self.assertEqual(self.game_screen.num_players, 3)
        # test to make sure it correctly switches to main game screen after number of players is selected
        self.assertEqual(self.stacked_widget.currentIndex(), 2)

    def test_back_button_switches_to_start_screen(self):
        # Set the current index to the game screen and then simulate the back button being pressed
        self.stacked_widget.setCurrentIndex(2)
        self.game_screen.back()
        self.assertEqual(self.stacked_widget.currentIndex(), 1)


class TestMainGameLogic(unittest.TestCase):
    def setUp(self):
        self.window = MainWindow()
        self.game_screen = self.window.game_screen
        self.game_screen.set_num_players(2)
        # initialize things like player pieces
        self.game_screen.initUI()

    def test_get_pixel_position(self):
        # Check a few known board positions.
        # For instance, position 1 should be at the bottom-left.
        x, y = self.game_screen.get_pixel_position(1)
        self.assertEqual((x, y), (0, 450))

        # Check a position in an odd row (positions 11-20) where the row goes right-to-left
        # For position 11, row = 1 and col = 0 (but since row 1 reverses, col becomes 9)
        x11, y11 = self.game_screen.get_pixel_position(11)
        self.assertEqual(x11, 9 * 50)

    def test_next_turn(self):
        # Simulate a spin result by setting the result manually
        self.game_screen.result = 4
        self.game_screen.current_player = 0
        # Reset positions to zero
        self.game_screen.player_positions = [0, 0, 0, 0]

        # Call next_turn to update position
        self.game_screen.next_turn()
        # The first player should have moved 4 spaces (assuming no chute/ladder at 4)
        expected_position = 4
        # If position 4 is a chute/ladder start, adjust based on CHUTES_LADDERS.
        if expected_position in CHUTES_LADDERS:
            expected_position = CHUTES_LADDERS[expected_position]
        self.assertEqual(self.game_screen.player_positions[0], expected_position)
        # Turn should now pass to player 2 (index 1)
        self.assertEqual(self.game_screen.current_player, 1)


if __name__ == "__main__":
    unittest.main()