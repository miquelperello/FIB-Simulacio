from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QWidget


class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('Button and Slots')

        self.label = QLabel(self)
        self.label.setText('Hello')
        self.label.move(10, 10)

        self.btn = QPushButton(self)
        self.btn.setText("Push here")
        self.btn.move(10, 50)
        self.btn.clicked.connect(self.btn_clicked)
        self.show()

    def btn_clicked(self):
        self.label.setText('Thanks for pressing')
        self.label.adjustSize()


def runGUI():

    app = QApplication([])

    cw = CustomWidget()

    app.exec_()


if __name__ == "__main__":
    runGUI()
