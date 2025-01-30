import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chutes and Ladders")
        self.setGeometry(500, 250, 500, 500)

        # label = QLabel("Hello", self)
        # label.setFont(QFont("Arial", 20))
        # label.setGeometry(0, 0, 500, 100)
        # label.setStyleSheet("color: #292929;"
        #                     "background-color: #6fdcf7;"
        #                     "font-weight: bold;"
        #                     "font-style: italic;"
        #                     "text-decoration: underline;")
        # label.setAlignment(Qt.AlignTop) # Vertically Top
        # label.setAlignment(Qt.AlignBottom)  # Vertically Bottom
        # label.setAlignment(Qt.AlignVCenter) # Vertically center
        # label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)  # Center & Top
        # label.setAlignment(Qt.AlignCenter) # Center and Center
        # label.setAlignment(Qt.AlignRight)

        self.setGeometry(500, 250, 500, 500)

        label1 = QLabel(self)
        label1.setGeometry(0, 0, 500, 500)

        pixmap = QPixmap("chutesandladders.jpg")
        label1.setPixmap(pixmap)
        label1.setScaledContents(True)

        label1.setGeometry((self.width() - label1.width()) // 2,
                           (self.height() - label1.height()) // 2,
                           label1.width(),
                           label1.height())




def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
