"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатие на кнопку
"""

from PySide6 import QtWidgets, QtGui
from hw_3_a_threads import WeatherHandler

class WeatherWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.threadFlag = False

        self.initUi()
        self.initSignals()

    def initUi(self) -> None:

        self.setWindowTitle("А что с погодой?")

        self.labelLatitude = QtWidgets.QLabel("Широта:")
        self.lineEditLatitude = QtWidgets.QLineEdit()
        self.lineEditLatitude.setText('60')

        layoutLatitude = QtWidgets.QHBoxLayout()
        layoutLatitude.addWidget(self.labelLatitude)
        layoutLatitude.addWidget(self.lineEditLatitude)

        self.labelLongitude = QtWidgets.QLabel("Долгота:")
        self.lineEditLongitude = QtWidgets.QLineEdit()
        self.lineEditLongitude.setText('30')

        layoutLongitude = QtWidgets.QHBoxLayout()
        layoutLongitude.addWidget(self.labelLongitude)
        layoutLongitude.addWidget(self.lineEditLongitude)

        self.labelSetDelay = QtWidgets.QLabel("Время задержки:")
        self.spinBoxSetDelay = QtWidgets.QSpinBox()
        self.spinBoxSetDelay.setValue(1)

        setDelayLayout = QtWidgets.QHBoxLayout()
        setDelayLayout.addWidget(self.labelSetDelay)
        setDelayLayout.addWidget(self.spinBoxSetDelay)

        self.resultTextEdit = QtWidgets.QTextEdit()
        self.resultTextEdit.setReadOnly(True)

        self.resultPushButton = QtWidgets.QPushButton("Начинаем узнавать...")

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(layoutLatitude)
        mainLayout.addLayout(layoutLongitude)
        mainLayout.addLayout(setDelayLayout)
        mainLayout.addWidget(self.resultTextEdit)
        mainLayout.addWidget(self.resultPushButton)

        self.setLayout(mainLayout)

    def initSignals(self) -> None:
        self.resultPushButton.clicked.connect(self.onResultPushButtonClickedTread)

    def onResultPushButtonClickedTread(self) -> None:

        if not self.threadFlag:
            self.resultPushButton.setText("Хватит с нас погоды!")
            self.threadGetWeather = WeatherHandler(self.lineEditLatitude.text(), self.lineEditLongitude.text())
            self.threadGetWeather.delay = self.spinBoxSetDelay.value()
            self.threadGetWeather.status = True
            self.threadGetWeather.start()
            self.lineEditLatitude.setEnabled(False)
            self.lineEditLongitude.setEnabled(False)
            self.spinBoxSetDelay.setEnabled(False)
            self.threadGetWeather.weatherResponsed.connect(self.getWeatherInfo)
            self.threadFlag = True
        else:
            self.threadGetWeather.status = False
            self.threadGetWeather.finished.connect(self.threadGetWeather.deleteLater)
            self.lineEditLatitude.setEnabled(True)
            self.lineEditLongitude.setEnabled(True)
            self.spinBoxSetDelay.setEnabled(True)
            self.resultPushButton.setText("Начинаем узнавать...")
            self.threadFlag = False

    def getWeatherInfo(self, data) -> None:
        self.resultTextEdit.setText(str(data))


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = WeatherWindow()
    window.show()

    app.exec()