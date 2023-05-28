"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""

from PySide6 import QtWidgets, QtGui
from hw_3_b_systeminfo_widget import SystemInfoWindow
from hw_3_c_wheatherapi_widget import WeatherWindow


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()

    def initUi(self) -> None:
        self.setWindowTitle("Всё и сразу")

        self.systemInfoWidget = SystemInfoWindow()
        self.weatherInfoWidget = WeatherWindow()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.systemInfoWidget)
        layout.addWidget(self.weatherInfoWidget)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()