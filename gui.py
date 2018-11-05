import sys  # sys нужен для передачи argv в QApplication
import desing  # Это наш конвертированный файл дизайна
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from workWithDataBase import DBManager
import time
from threading import Thread
import subprocess
import os

PACH_DB = r'C:\projectTree\database.db'
SETTING_PC = 'PC1'

tableColumns = ["ID", "ФИО", "Сервер", "Процесс Photoscan", "Процесс ArGis", "Построения отчера", "Отправка отчета"]
ListToolTip = ["Порядковый номаер процесса", "Фамилия имя Отчество заказчика", "Этапы выполнения сервером Например загрузка данных"]

class MainGui(QtWidgets.QMainWindow, desing.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.db = DBManager(PACH_DB, SETTING_PC)

        #Получаем настройки
        self.settings = self.db.getSettings()

        #Отрисовка таблицы
        self.tableWidget.setColumnCount(len(tableColumns))  # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        self.tableWidget.setHorizontalHeaderLabels(tableColumns)

        #Установить подсказки
        self.setToolTipTable(ListToolTip)

        # заполняем
        self.ThreadUpdateTableState = True
        self.ThreadUpdateTable = Thread(target=self.updateTable, args=(1,))
        self.ThreadUpdateTable.start()

        self.tableWidget.resizeColumnsToContents()

        # при нажатии кнопки
        self.action.triggered.connect(self.OnClickOpenDB)
        self.action_4.triggered.connect(self.OnClickExit)

        self.pushButton.clicked.connect(self.OnClickOpenProjectPhotoscan)


    def setToolTipTable(self, ListToolTip):
        '''
        Устанавливаем подсказки согластно списку
        :param ListToolTip:
        :return:
        '''
        for index, tip in enumerate(ListToolTip):
            self.tableWidget.horizontalHeaderItem(index).setToolTip(tip)
            self.tableWidget.horizontalHeaderItem(index).setTextAlignment(QtCore.Qt.AlignHCenter)

    def OnClickOpenDB(self):
        print("Отрытия базы данных")

    def OnClickExit(self):
        '''
        Программа выхода из програмы
        :return:
        '''
        #self.t1._stop()
        self.ThreadUpdateTableState = False
        sys.exit()

    def OnClickOpenProjectPhotoscan(self):
        '''
        открывает капку с проектом
        :return:
        '''
        pachProject = self.settings[0][1]  #Получаем путь до проектов

        art = os.getcwd()+'/openDir.BAT ' + pachProject + '/ID_'+str(self.selectedID)
        p5 = subprocess.Popen(art, shell=True, stdout=subprocess.PIPE)

    def updateTable(self, delay):
        while self.ThreadUpdateTableState:
            self.__updateTable()
            self.tableWidget.resizeColumnsToContents()

            row = self.tableWidget.currentRow()  # Получаем выделенный столбец
            self.selectedID = self.tableWidget.item(row, 0).text()  # Получаем ID

            self.label.setText("ID пользователя: " + self.selectedID)
            time.sleep(delay)

    def __updateTable(self):
        '''
        Обнавляет показатели таблицы в GUI
        :return:
        '''
        allUserID = self.db.getAllUniqueUsers()  #Получаем всех ID процессы
        self.tableWidget.setRowCount(len(allUserID))

        for index, userId in enumerate(allUserID):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(str(userId)))

            for i in self.db.dictProcessingPhotoscan["Server"]:
                process = self.db.dictProcessingPhotoscan["Server"][i]
                stateProcess = self.db.getNeedProcessingServer(userId, process)

                if stateProcess:
                    #True
                    self.tableWidget.setItem(index, 2, QTableWidgetItem(
                        self.db.dictProcessingUserManager['Server'][i] + " - OK"))
                else:
                    # False
                    self.tableWidget.setItem(index, 2, QTableWidgetItem(
                        self.db.dictProcessingUserManager['Server'][i] + " - В процессе"))
                    break
                if stateProcess == "error":
                    # error
                    self.tableWidget.setItem(index, 2, QTableWidgetItem(
                        self.db.dictProcessingUserManager['Server'][i] + " - Еще не начался"))
                    break

            for i in self.db.dictProcessingPhotoscan["Photoscan"]:
                process = self.db.dictProcessingPhotoscan["Photoscan"][i]

                stateProcess = self.db.getNeedProcessing(userId, process)

                #self.tableWidget.setItem(index, 4, QTableWidgetItem(str(stateProcess)+ " process = "+ process))

                if stateProcess == "error":
                    # error
                    self.tableWidget.setItem(index, 3, QTableWidgetItem(
                        self.db.dictProcessingUserManager['Photoscan'][i] + " - Еще не начался"))
                    break

                if stateProcess:
                    #True
                    self.tableWidget.setItem(index, 3, QTableWidgetItem(
                        self.db.dictProcessingUserManager['Photoscan'][i] + " - OK"))

                else:
                    # False
                    self.tableWidget.setItem(index, 3, QTableWidgetItem(
                        self.db.dictProcessingUserManager['Photoscan'][i] + " - В процессе"))
                    break



def main():
    QtGui.QGuiApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainGui()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()