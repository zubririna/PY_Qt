"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""

from PySide6 import QtWidgets, QtGui
from hw_3_a_threads import SystemInfo


class SystemInfoWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initThreads()
        self.initUi()
        self.initSignals()

    def initThreads(self) -> None:
        self.threadSystemInfo = SystemInfo()
        self.threadSystemInfo.status = True
        self.threadSystemInfo.start()

    def initUi(self):

        self. setWindowTitle("System Info")

        self.labelCPU = QtWidgets.QLabel("CPU:")
        self.lineEditCPU = QtWidgets.QLineEdit()
        self.lineEditCPU.setEnabled(False)

        layoutCPU = QtWidgets.QHBoxLayout()
        layoutCPU.addWidget(self.labelCPU)
        layoutCPU.addWidget(self.lineEditCPU)

        self.labelRAM = QtWidgets.QLabel("RAM:")
        self.lineEditRAM = QtWidgets.QLineEdit()
        self.lineEditRAM.setEnabled(False)

        layoutRAM = QtWidgets.QHBoxLayout()
        layoutRAM.addWidget(self.labelRAM)
        layoutRAM.addWidget(self.lineEditRAM)

        self.labelSetDelay = QtWidgets.QLabel("Set delay:")
        self.spinBoxSetDelay = QtWidgets.QSpinBox()

        setDelayLayout = QtWidgets.QHBoxLayout()
        setDelayLayout.addWidget(self.labelSetDelay)
        setDelayLayout.addWidget(self.spinBoxSetDelay)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(layoutCPU)
        mainLayout.addLayout(layoutRAM)
        mainLayout.addLayout(setDelayLayout)

        self.setLayout(mainLayout)

    def initSignals(self) -> None:
        self.spinBoxSetDelay.valueChanged.connect(self.spinBoxChanged)
        self.threadSystemInfo.systemInfoReceived.connect(self.getSystemInfo)

    def spinBoxChanged(self) -> None:
        self.threadSystemInfo.delay = self.spinBoxSetDelay.value()

    def getSystemInfo(self, data: list) -> None:
        self.lineEditCPU.setText(f"{data[0]}%")
        self.lineEditRAM.setText(f"{data[1]}%")


if __name__ == '__main__':
    app = QtWidgets.QApplication()

    window = SystemInfoWindow()
    window.show()

    app.exec()