"""
Модуль в котором содержаться потоки Qt
"""

import time
import psutil
import requests.exceptions
from PySide6 import QtCore


class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.Signal(list)  # TODO Создайте экземпляр класса Signal и передайте ему в конструктор тип данных передаваемого значения (в текущем случае list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None  # TODO создайте атрибут класса self.delay = None, для управлением задержкой получения данных
        self.status = None

    def run(self) -> None:  # TODO переопределить метод run
        if self.delay is None:  # TODO Если задержка не передана в поток перед его запуском
            self.delay = 1  # TODO то устанавливайте значение 1

        while self.status:  # TODO Запустите бесконечный цикл получения информации о системе
            cpu_value = psutil.cpu_percent()  # TODO с помощью вызова функции cpu_percent() в пакете psutil получите загрузку CPU
            ram_value = psutil.virtual_memory().percent  # TODO с помощью вызова функции virtual_memory().percent в пакете psutil получите загрузку RAM
            self.systemInfoReceived.emit([cpu_value, ram_value])  # TODO с помощью метода .emit передайте в виде списка данные о загрузке CPU и RAM
            time.sleep(self.delay)  # TODO с помощью функции .sleep() приостановите выполнение цикла на время self.delay


class WeatherHandler(QtCore.QThread):
    weatherResponsed = QtCore.Signal(dict)   # TODO Пропишите сигналы, которые считаете нужными

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)

        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.__delay = 10
        self.__status = None

    @property
    def status(self) -> bool:
        return self.__status

    @status.setter
    def status(self, value) -> None:
        self.__status = value

    @property
    def delay(self) -> int:
        return self.__delay

    @delay.setter
    def delay(self, delay_) -> None:
        self.__delay = delay_

    def run(self) -> None:   # TODO настройте метод для корректной работы

        while self.__status:
            try:
                response = requests.get(self.__api_url)
            except requests.exceptions.ConnectionError:
                self.weatherResponsed.emit('No internet connection')
                time.sleep(1)
            else:
                data = response.json()
                self.weatherResponsed.emit(data)
                time.sleep(self.__delay)