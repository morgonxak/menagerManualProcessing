import sys  # sys нужен для передачи argv в QApplication
import desing  # Это наш конвертированный файл дизайна
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem


PACH_DB = r'C:\projectTree\database.db'
SETTING_PC = 'PC1'

class MainGui(QtWidgets.QMainWindow, desing.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна


        # при нажатии кнопки
        self.action.triggered.connect(self.OnClickOpenDB)


    def OnClickOpenDB(self):
        print("Отрытия базы данных")
        self.tableWidget.setColumnCount(7)  # Устанавливаем три колонки
        self.tableWidget.setRowCount(2)  # и одну строку в таблице

        # Устанавливаем заголовки таблицы
        self.tableWidget.setHorizontalHeaderLabels(["ID", "ФИО", "Сервер", "Процесс Photoscan", "Процесс ArGis", "Построения отчера", "Отправка отчета"])
        self.tableWidget.horizontalHeaderItem(0).setToolTip("Column 1 ")

        # Устанавливаем выравнивание на заголовки
        self.tableWidget.horizontalHeaderItem(0).setTextAlignment(QtCore.Qt.AlignLeft)
        self.tableWidget.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignHCenter)
        self.tableWidget.horizontalHeaderItem(2).setTextAlignment(QtCore.Qt.AlignRight)

        # заполняем
        self.tableWidget.setItem(0, 0, QTableWidgetItem("Text in column 1"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Text in column 2"))
        self.tableWidget.setItem(0, 2, QTableWidgetItem("Text in column 3"))

        #self.tableWidget.setFlags(QtCore.Qt.ItemIsEnabled)

        self.tableWidget.resizeColumnsToContents()

    def __updateTable(self):
        '''
        Обнавляет показатели таблицы в GUI
        :return:
        '''
        pass


def main():
    QtGui.QGuiApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainGui()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()