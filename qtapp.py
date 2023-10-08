from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PIL import ImageQt
from mymodel import *


WINDOW_SIZE = 550, 300


class MainWindow(QWidget):
    """Главное окно"""

    def __init__(self):
        """Конструктор интерфейса"""

        super().__init__(None)
        self.create_model(train=False)
        self.initGUI()

    def initGUI(self):
        """Конструктор интерфейса"""

        self.canvas = Canvas(self)
        self.clear_button = ClearButton(self)
        self.scan_button = ScanButton(self)
        self.answer = QLabel(text='')
        self.answer.setStyleSheet("""
            QLabel {
                color: red;
                font-size: 15px;
                font-weights: 2000;
            }
        """)
        layout = QGridLayout()

        layout.addWidget(self.clear_button, 0, 0)
        layout.addWidget(self.scan_button, 1, 0)
        layout.addWidget(self.answer, 2, 0)
        layout.addWidget(self.canvas, 0, 1, 0, 2)

        self.setLayout(layout)
        self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.show()

    def create_model(self, train: bool = True):
        """Создание модели нейронной сети"""

        self.model = MyModel(train)


class Canvas(QLabel):
    """Канвас для рисования"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.last_x, self.last_y = None, None
        canv = QPixmap(300, 300)
        canv.fill(Qt.white)
        self.setPixmap(canv)

    def mouseMoveEvent(self, event):
        """Движение мышкой"""

        if self.last_x is None:
            self.last_x = event.x()
            self.last_y = event.y()
            return

        qp = QPainter(wnd.canvas.pixmap())
        pen = QPen()
        pen.setWidth(20)
        qp.setPen(pen)

        qp.drawLine(self.last_x, self.last_y, event.x(), event.y())
        qp.end()
        wnd.update()

        self.last_x = event.x()
        self.last_y = event.y()

    def mouseReleaseEvent(self, event):
        """Подьем мыши"""

        self.last_x = None
        self.last_y = None


class ClearButton(QPushButton):
    """Кнопка очистки канваса"""

    def __init__(self, *args, **kwargs):
        super().__init__(text='Очистить', *args, **kwargs)

        self.clicked.connect(self.onclick)

    @staticmethod
    def onclick(event):
        """Клик"""

        canv = QPixmap(300, 300)
        canv.fill(Qt.white)
        wnd.canvas.setPixmap(canv)
        wnd.answer.setText('')


class ScanButton(QPushButton):
    """Кнопка для сканирования рисунка"""

    def __init__(self, *args, **kwargs):
        super().__init__(text='Сканировать', *args, **kwargs)

        self.clicked.connect(self.onclick)

    @staticmethod
    def onclick(event):
        """Клик"""

        qimage = wnd.canvas.pixmap().toImage()

        image = ImageQt.fromqimage(qimage)
        image = image.resize((28, 28))
        image = image.convert('L')
        data_image = np.asarray(image)

        convert_image = wnd.model.convert_image(data_image)
        res = wnd.model.use_model(convert_image)

        wnd.answer.setText(f'Я думаю это цифра {np.argmax(res)}!\n'
                           f'Вероятность: {round(np.max(res) / np.sum(res) * 100, 2)}%')


if __name__ == '__main__':
    app = QApplication()
    wnd = MainWindow()
    app.exec_()
