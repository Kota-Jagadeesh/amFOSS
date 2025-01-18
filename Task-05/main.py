import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PySide6.QtGui import QPixmap,QMovie
from PySide6.QtCore import  QRect
from search_window import SearchWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.w = None

    def initUI(self):
        self.setWindowTitle("Pokédex")

        self.setFixedSize(850, 500)

        self.setStyleSheet("""
            QPushButton {
                background-color: dark-grey;
                color: white;
                border: 1px solid #BA263E;
                font: bold 16px;
                text-align: center;
                border-radius: 10px;
            }
            QMainWindow {
                background-color: black;
            }
            QLabel {
                font-size: 32px;
            }
            QPushButton:hover {
                background-color: #BA263E;
                color: dark-grey;
            }
        """)

        labelmov = QLabel(self)
        labelmov.setScaledContents(True)
        movie = QMovie("../assets/openingpokeball-pokemon.gif")
        labelmov.setGeometry(QRect(0, 0, 900,478))
        labelmov.setMovie(movie)
        movie.start() 
        poke_search_label = QLabel("POKÉSEARCH", self)
        poke_search_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        poke_search_label.setGeometry(QRect(50, 5, 900, 250))
        poke_label = QLabel("ENGINE ", self)
        poke_label.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        poke_label.setGeometry(QRect(50, 50, 900, 250))

        pushButton = QPushButton(parent=self, text='GO!')
        pushButton.setGeometry(50, 300, 160, 43)
        pushButton.clicked.connect(self.open_search_window)
    
        self.labelpic = QLabel(self)
        self.labelpic.setGeometry(QRect(400, 20, 550, 700))
        self.labelpic.setPixmap(QPixmap(""))
        self.labelpic.setScaledContents(True)

        self.show()
      
    def open_search_window(self, checked):
        if self.w is None:
            self.w = SearchWindow()
        self.w.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
