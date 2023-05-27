"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings.ui)

Программа должна обладать следующим функционалом:

1. Добавить для Qdial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtCore, QtGui
from hw_2.ui.d_eventfilter_settings import Ui_Form

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.initUi()
        self.initSignals()

    def initUi(self):
        save_combo_box = QtCore.QSettings ("save_combo_box")
        print(save_combo_box.value("text", "dec"))
        save_dial = QtCore.QSettings ("save_dial")
        print(save_dial.value ("text", "0"))

        self.minValue = 0
        self.maxValue = 50

        self.ui.dial.setMinimum(self.minValue)
        self.ui.dial.setMaximum(self.maxValue)

        self.ui.horizontalSlider.setMinimum(self.minValue)
        self.ui.horizontalSlider.setMaximum(self.maxValue)

        self.ui.comboBox.addItems(['dec', 'oct', 'hex', 'bin'])

        self.ui.lcdNumber.setDigitCount(6)

        self.ui.comboBox.setCurrentText(save_combo_box.value("text", "dec"))
        self.ui.dial.setSliderPosition(int(str(save_dial.value("text", "0"))))
        self.ui.horizontalSlider.setSliderPosition(int(str(save_dial.value("text", "0"))))
        self.ui.lcdNumber.display (self.dialConv(self.ui.dial.value()))

    def initSignals(self):
        self.ui.horizontalSlider.valueChanged.connect(self.onHorizontalSliderVC)
        self.ui.dial.valueChanged.connect(self.onDialVC)
        self.ui.comboBox.currentTextChanged.connect(self.onComboBoxCTC)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.text() == '+':
            self.ui.dial.setSliderPosition(self.ui.dial.value() + 1)
            print (self.ui.dial.value())
        if event.text() == '-':
            self.ui.dial.setSliderPosition(self.ui.dial.value() - 1)
            print (self.ui.dial.value())

    def dialConv(self, val: int):
        if self.ui.comboBox.currentText() == "dec":
            return int(val)
        if self.ui.comboBox.currentText() == "oct":
            return oct(val)
        if self.ui.comboBox.currentText() == "hex":
            return hex(val)
        if self.ui.comboBox.currentText() == "bin":
            return bin(val)

    def onHorizontalSliderVC(self):
        self.ui.dial.setSliderPosition(self.ui.horizontalSlider.value())
        self.ui.lcdNumber.display(self.dialConv(self.ui.horizontalSlider.value()))

    def onDialVC(self):
        self.ui.horizontalSlider.setSliderPosition(self.ui.dial.value())
        self.ui.lcdNumber.display(self.dialConv(self.ui.dial.value()))

    def onComboBoxCTC(self):
        self.ui.lcdNumber.display(self.dialConv(self.ui.dial.value()))

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()