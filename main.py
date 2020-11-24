# -*- coding: utf-8 -*-
import sys
import threading
import urllib.request as urlreq
# import re
import time
import datetime
from bs4 import BeautifulSoup


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QAbstractScrollArea
from PyQt5.QtGui import QIcon, QBrush, QColor
from UI_main import Ui_MainWindow
from DM_ManagerTeams import DM_ManagerTeams

class TournamentsWotCheck(QtWidgets.QMainWindow):
    def __init__(self):
        super(TournamentsWotCheck, self).__init__()
        # UI main
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()

        # UI Manager Teams
        self.ui_DM_ManagerTeams = DM_ManagerTeams()

        # Objects
        self.leftVal = 0
        self.fromSpinBoxVal = self.ui.spinBox_From.value()
        self.toSpinBoxVal = self.ui.spinBox_To.value()
        self.threadsNumber = 1

        self.lock = threading.Lock()

        self.listUrlsTournaments = []
        self.listHandeledData = []
        self.listUrlsTournaments.clear()
        self.listHandeledData.clear()

        # Re
        # self.RE_Title = r"<title>[\w\d\s\S]*<[\/]title>"

    def init_UI(self):
        self.init_connects()
        self.init_Table()
        # Other
        self.setWindowIcon(QIcon("icon.png"))

    def init_connects(self):
        # Changs spinBox
        self.ui.spinBox_From.textChanged.connect(self.updateValFromToOf)
        self.ui.spinBox_To.textChanged.connect(self.updateValFromToOf)

        self.ui.spinBox_Treads.textChanged.connect(self.updateThreads)
        # Button(s)
        self.ui.pushButton_pwned.clicked.connect(self.runButton)

        # Actions
        self.ui.actionDownload_data_all_team_in_tournament.triggered.connect(self.createDMWindow)

    def createDMWindow(self):
        self.ui_DM_ManagerTeams.show()

    def init_Table(self):
        self.ui.tableWidget.clear()

        self.ui.tableWidget.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.ui.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.ui.tableWidget.setColumnCount(6)
        self.ui.tableWidget.setRowCount(0)

        self.ui.tableWidget.setHorizontalHeaderLabels(["Title", "Prize", "Url", "Data", "Confirmed", "Server"])
        self.ui.tableWidget.setSortingEnabled(True)

        # self.ui.tableWidget.resizeColumnsToContents()

    def updateValFromToOf(self):
        # Update var
        self.fromSpinBoxVal = self.ui.spinBox_From.value()
        self.toSpinBoxVal = self.ui.spinBox_To.value()
        self.leftVal = self.toSpinBoxVal - self.fromSpinBoxVal + 1
        # Update UI
        self.ui.label_Of.setText(str(self.leftVal))

    def updateThreads(self):
        self.threadsNumber = self.ui.spinBox_Treads.value()

    def createListUrlsTournaments(self):
        # https://worldoftanks.ru/ru/tournaments/17165/
        self.listUrlsTournaments.clear()

        i = self.fromSpinBoxVal
        data = ""
        while i <= self.toSpinBoxVal:
            data = "https://worldoftanks.ru/ru/tournaments/" + str(i) + "/"
            self.listUrlsTournaments.append(data)
            i += 1
        self.listUrlsTournaments.reverse()

    def decodeReq(self, str):
        return str.decode('utf8')

    def req(self, url):
        # Do request and return text getted responce in utf-8
        user_agent = "Kirill Ignatenko hello ^^ . This is a parser from _TToJIoHuu_210_. vk.com/againuarehere ."
        headers = {'User-Agent': user_agent}

        try:
            rq = urlreq.Request(url,headers=headers)
            responce = urlreq.urlopen(rq)
            resp = responce
            statusCode = resp.getcode()
        except:
            # При большом кол-ве потоков часто вылетает 404, когда на самом деле там не 404
            # Может быть не хватает скорости интернета, не знаю точно
            statusCode = 404
        responseText = "FAIL"
        if(statusCode != 404):
            buff = resp.read()
            responseText = self.decodeReq(buff)
        return responseText

    def handleListUrls(self):
        threadsCount = self.threadsNumber
        threads_list = []
        for i in range(threadsCount):
            my_thread = threading.Thread(target=self.worker)
            threads_list.append(my_thread)
        for t in threads_list:
            try:
                t.start()
            except:
                print("Error t.start() " + t.getName())
        for t in threads_list:
            try:
                t.join()
            except:
                print("Error t.join() " + t.getName())

    def worker(self):
        # Once send req and handle getted responce
        while len(self.listUrlsTournaments) > 0:

            self.lock.acquire()

            if len(self.listUrlsTournaments) > 0:
                url = self.listUrlsTournaments.pop()

                self.lock.release()

                self.ui.label_Of.setText(str(self.leftVal - 1))
                self.leftVal -= 1
                self.setOfLabel(self.leftVal)
                resp = self.req(url)

                if resp != "FAIL":
                    # listFinded_RE_Title = re.findall(self.RE_Title, resp)
                    # title = listFinded_RE_Title[0]
                    # title = title[7:-8]
                    # data = [title, url]
                    data = {"title": None,
                            "url": None,
                            "prize": None,
                            "confirmed": None,
                            "server": None,
                            "date_tournament": None}
                    # data["title"] = title
                    self.lock.acquire()
                    data["url"] = url
                    ################################ BeautifulSoup
                    soup = BeautifulSoup(resp, "html.parser")
                    # Title
                    try:
                        data["title"] = soup.find("span", class_="header-inner_name").get_text(strip=True)
                    except:
                        data["title"] = "Error title"
                    # Prize
                    try:
                        data["prize"] = soup.find("span", class_="ico-prize").parent.parent.find("span", class_="tournament-info-list_description").get_text(strip=True)
                        if data["prize"] == "Личные резервы (доп. опыт; доп. опыт экипажа; доп. кредиты)":
                            data["prize"] = "Личные резервы"
                    except:
                        data["prize"] = "None"
                    # Confirmed
                    try:
                        data["confirmed"] = soup.find("span", class_="ico-confirmed").parent.parent.find("span", class_="tournament-info-list_description").get_text(strip=True)
                        data["confirmed"] = data["confirmed"].replace(' ', '')
                    except:
                        data["confirmed"] = "None"
                    # Server
                    try:
                        data["server"] = soup.find("span", class_="ico-region").parent.parent.find("span", class_="tournament-info-list_description").get_text(strip=True)
                        data["server"] = data["server"].replace(' ', '')
                        data["server"] = data["server"].replace('\n', '')
                        data["server"] = data["server"].replace('\t', '')
                    except:
                        data["server"] = "None"
                    # Data tournament
                    try:
                        timestamp = soup.find("span", class_="header-inner_status js-tournament-schedule")["data-start-date"]
                        timestampFloat = float(timestamp)
                        val = datetime.datetime.fromtimestamp(timestampFloat).strftime('%Y.%m.%d %H:%M')
                        data["date_tournament"] = val
                    except:
                        try:
                            timestamp = soup.find("span", class_="tournament-heading_small js-tournament-schedule")["data-start-date"]
                            timestampFloat = float(timestamp)
                            val = datetime.datetime.fromtimestamp(timestampFloat).strftime('%Y.%m.%d %H:%M')
                            data["date_tournament"] = val
                        except:
                            data["date_tournament"] = "None"
                    ################################ BeautifulSoup


                    self.listHandeledData.append(data.copy())
                    self.lock.release()
            else:
                self.lock.release()


                    # listFinded_RE_Title.clear()

    def setOfLabel(self, data):
        self.ui.label_Of.setText(str(data))

    def fillTableAll(self, listData: list):
        self.ui.tableWidget.setRowCount(int(len(listData)))
        counterRow = 0
        # Баг --> по какой-то причине, при повторном запуске скана и заполнении таблицы, повторном, некоторые данные в словаре перестают быть типа str ИЛИ передаваыемые данные в объект изменяют свой тип
        for item in listData:
            # Title
            it = QTableWidgetItem(str(item["title"]))
            it.setForeground(QBrush(QColor(230, 230, 230)))
            # it.setBackground(QBrush(QColor(115,26,21)))
            self.ui.tableWidget.setItem(counterRow, 0, it)
            # Prizes
            it = QTableWidgetItem(str(item["prize"]))
            it.setForeground(QBrush(QColor(245,216,25)))
            self.ui.tableWidget.setItem(counterRow, 1, it)
            # Url
            it = QTableWidgetItem(str(item["url"]))
            it.setForeground(QBrush(QColor(174,174,174)))
            self.ui.tableWidget.setItem(counterRow, 2, it)
            # Data tournament
            it = QTableWidgetItem(str(item["date_tournament"]))
            it.setForeground(QBrush(QColor(220, 220, 220)))
            self.ui.tableWidget.setItem(counterRow, 3, it)
            # Confirmed
            it = QTableWidgetItem(str(item["confirmed"]))
            it.setForeground(QBrush(QColor(46,165,223)))
            self.ui.tableWidget.setItem(counterRow, 4, it)
            # Server
            it = QTableWidgetItem(str(item["server"]))
            it.setForeground(QBrush(QColor(220, 220, 220)))
            self.ui.tableWidget.setItem(counterRow, 5, it)

            # if (str(item["title"]) == ""):
            #     print("title error ", str(item["title"]))
            #
            # if (str(item["prize"]) == ""):
            #     print("prize error ", str(item["prize"]))
            #
            # if (str(item["url"]) == ""):
            #     print("url error ", str(item["url"]))
            #
            # if (str(item["date_tournament"]) == ""):
            #     print("date_tournament error ", str(item["date_tournament"]))
            #
            # if (str(item["confirmed"]) == ""):
            #     print("confirmed error ", str(item["confirmed"]))
            #
            # if (str(item["server"]) == ""):
            #     print("server error ", str(item["server"]))


            counterRow += 1

        # self.ui.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.ui.tableWidget.resizeColumnsToContents()
        self.ui.tableWidget.resizeRowsToContents()

    def runButton(self):
        tr = threading.Thread(target=self.run)
        tr.start()

    def run(self):
        # Clear data

        self.init_Table()

        self.listHandeledData.clear()
        self.listUrlsTournaments.clear()

        # Processing obj-s
        self.createListUrlsTournaments()
        self.ui.tableWidget.setRowCount(len(self.listUrlsTournaments))

        # Network handle
        threadRun = threading.Thread(target=self.handleListUrls)

        try:
            threadRun.start()
            try:
                threadRun.join()
            except:
                print("threadRun error")
        except:
            print("threadRun error")


        self.fillTableAll(self.listHandeledData)

app = QtWidgets.QApplication([])
application = TournamentsWotCheck()
# application.setWindowFlag(QtCore.Qt.FramelessWindowHint) убирает рамку всю
application.show()
sys.exit(app.exec())