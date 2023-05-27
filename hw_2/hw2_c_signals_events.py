"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
# 3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""

import time
from PySide6 import QtWidgets, QtGui, QtCore
from hw_2.ui.c_signals_events import Ui_Form

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.initSignals()

    def initSignals(self):

        self.ui.pushButtonLT.clicked.connect(self.onPushButtonLTClicked)
        self.ui.pushButtonRT.clicked.connect(self.onPushButtonRTClicked)
        self.ui.pushButtonCenter.clicked.connect(self.onPushButtonCenterClicked)
        self.ui.pushButtonLB.clicked.connect(self.onPushButtonLBClicked)
        self.ui.pushButtonRB.clicked.connect(self.onPushButtonRBClicked)

        self.ui.pushButtonMoveCoords.clicked.connect(self.onPushButtonMoveCoords)

        self.ui.pushButtonGetData.clicked.connect(self.getWindowInfo)

    def screenSize(self):

        a = self.screen().geometry().width()
        b = self.screen().geometry().height()
        return (a, b)

    def windowSize(self):

        a = self.size().width()
        b = self.size().height()
        return (a, b)

    def onPushButtonLTClicked(self): #вверх влево

        x = 0
        y = 0
        self.move(x, y)

    def onPushButtonRTClicked(self): #вверх вправо

        scr_width, scr_height = self.screenSize()
        wind_width, wind_height = self.windowSize()
        x = scr_width - wind_width
        y = 0
        self.move(x, y)

    def onPushButtonCenterClicked(self):

        scr_width, scr_height = self.screenSize()
        wind_width, wind_height = self.windowSize()
        x = (scr_width / 2) - (wind_width / 2)
        y = (scr_height / 2) - (wind_height / 2)
        self.move(x, y)

    def onPushButtonLBClicked(self): #вниз влево

        scr_width, scr_height = self.screenSize()
        wind_width, wind_height = self.windowSize()
        x = 0
        y = scr_height - wind_height
        self.move(x, y)

    def onPushButtonRBClicked(self): #вниз вправо

        scr_width, scr_height = self.screenSize()
        wind_width, wind_height = self.windowSize()
        x = scr_width - wind_width
        y = scr_height - wind_height
        self.move(x, y)

    def onPushButtonMoveCoords(self):

        x = self.ui.spinBoxX.value()
        y = self.ui.spinBoxY.value()
        self.move(x, y)

    def windowState(self):

        window_state = 'Окно'
        if self.isHidden():
            window_state = 'Окно свернуто'
        elif self.isActiveWindow():
            window_state = 'Окно активно'
        elif self.isVisible():
            window_state = 'Окно отображено'
        elif self.isFullScreen():
            window_state = 'Окно развернуто (полный экран)'
        return (window_state)

    def getWindowInfo(self):

        self.ui.plainTextEdit.setPlainText(f'{time.ctime()}\n'
                                            f'Количество экранов: {len(QtWidgets.QApplication.screens())}\n'
                                            f'Текущее основное окно: {self.objectName()}\n'
                                            f'Разрешение экрана: {self.screen().geometry().width()}, {self.screen().geometry().height()}\n'
                                            f'Окно находится на экране: {self.screen().name()}\n'
                                            f'Размер окна: {self.geometry().width()}, {self.geometry().height()}\n'
                                            f'Минимальный размер окна: {self.minimumSize().width()}, {self.minimumSize().height()}\n'
                                            f'Текущее положение окна: {self.x()}, {self.y()}\n'
                                            f'Координаты центра приложения: {self.x() + self.geometry().width()/2}, {self.y() + self.geometry().height()/2}\n'
                                            f'Состояние окна: {self.windowState()}')



    def moveEvent(self, event: QtGui.QMoveEvent) -> None:

        print(f'{time.ctime()} Начальное положение окна: {event.oldPos()}')
        print(f'{time.ctime()} Новое положение окна: {event.pos()}')
        print()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:

        print(f'{time.ctime()} Начальный размер окна: {event.oldSize()}')
        print(f'{time.ctime()} Новый размер окна: {event.size()}')
        print()



if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()