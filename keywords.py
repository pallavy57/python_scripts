
from functools import partial
import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import csv
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from os.path import exists



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(0, 0, 1300, 900)
        self._createMenuBar()
        self.show()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # editMenu = menuBar.addMenu("&Edit")
        # helpMenu = menuBar.addMenu("&Help")
        quit = QAction("Search", self)
        menuBar.addAction(quit)
        menuBar.triggered[QAction].connect(self.openSearch)
        self.setWindowTitle("Keyword Suggestions and Dissections")

    def leftarea(self):
        self.dock = QDockWidget("Search Keywords", self)
        self.dock.setMaximumHeight(900)
        self.dock.setMaximumWidth(500)
        self.dock.setFloating(False)
        # self.setCentralWidget(QTextEdit())

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
        self.setWindowTitle("Keyword Searching Tool")
        # Scroll Area Properties

        search_form = QWidget()
        layout = QFormLayout(search_form)
        search_form.setLayout(layout)
        self.search_term = QLineEdit(search_form)
        self.search_term.setPlaceholderText("Enter a search term")
        layout.addRow(self.search_term)
        
        self.search_term.textChanged.connect(
            lambda param1, arg1=layout: self.onChanged(param1, arg1))

        btn_search = QPushButton('Go', clicked=self.buttonClicked)
        layout.addRow(btn_search)
        self.dock.setWidget(search_form)
        self.dock.move(20, 20)
        self.dock.resize(900, 40)
        self.dock.show()

    def rightarea(self, dummmy):
        self.dock = QDockWidget("See Statistics", self)
        self.dock.setMaximumHeight(900)
        self.dock.setMaximumWidth(900)
        self.dock.setFloating(False)
        # self.setCentralWidget(QTextEdit())
        print("Show this")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        self.setWindowTitle("Keyword Searching Tool")

        y1 = []

        # create horizontal list i.e x-axis
        x = []

        with open('searches.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                x.append(row[0])
                y1.append(int(row[1]))
        print(y1, x)
        # creating a pyqtgraph plot window
        window = pg.plot()

        window.setBackground("w")
        xval = list(range(1, len(x)+1))
        ticks = []
        for i, item in enumerate(x):
            ticks.append((xval[i], item))
        ticks = [ticks]
        bargraph = pg.BarGraphItem(x=xval, height=y1, width=0.5)
        window.addItem(bargraph)
        ax = window.getAxis('bottom')
        ax.setTicks(ticks)
        self.dock.setWidget(window)

        self.dock.move(20, 20)
        self.dock.resize(90, 40)
        self.dock.show()

    def downarea(self, dummmy):
        self.dock = QDockWidget("See Statistics", self)
        self.dock.setMaximumHeight(200)
        self.dock.setMaximumWidth(900)
        self.dock.setFloating(False)
        # self.setCentralWidget(QTextEdit())
        print("Show this")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        self.setWindowTitle("Keyword Searching Tool")
        table = dict()
        with open('searches.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                table[row[0]] = row[1]
        tableList = []
        for key, value in table.items():
            tableList.append({
                "Name": key,
                "count": value
            })
        self.tableWidget = QTableWidget()
        # # Row count

        # Column count
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 150)
        # # self.tableWidget.setColumnWidth(2, 50)

        self.tableWidget.setHorizontalHeaderLabels(tableList[0].keys())
        self.tableWidget.setRowCount(len(tableList))

        row = 0
        for e in tableList:
            print(e)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(e["Name"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(e["count"]))

            row += 1

        # Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)
        self.dock.setWidget(self.tableWidget)

        self.dock.move(20, 20)
        self.dock.resize(90, 40)
        self.dock.show()

    def openSearch(self):
        self.leftarea()
        file_exists = exists("searches.csv")
        if file_exists == True:
            self.downarea(self)

    def onChanged(self, param1, arg1):
        self.show_edit = QLabel()
        trends = TrendReq()
        keyword = trends.suggestions(keyword=param1)
        data = pd.DataFrame(keyword)

        if data.head().empty:
            self.show_edit.setText("No Matches Found")
            arg1.addRow(self.show_edit)
            self.show_edit.show()

        if (len(keyword) != 0):
            self.show_edit.setText(str(data.head()["title"][0]))
            arg1.insertRow(data['title'].size, self.show_edit)
            self.show_edit.show()
            self.show_edit.mousePressEvent = self.buttonClicked
            self.show_edit.mousePressEvent = partial(
                self.buttonClicked, self.show_edit, str(data.head()["title"][0]))

        else:
            self.show_edit.setText("No Matches Found")
            arg1.addRow(self.show_edit)
            self.show_edit.show()

    def buttonClicked(self, edit, text, e):

        trends = TrendReq()
        trends.build_payload(kw_list=[text])
        data = trends.interest_by_region()

        df = data.head(10)
        print(df)
        with open('searches.csv', 'w', encoding="utf-8", newline='') as fileObj:
            # Creater a CSV writer object
            writerObj = csv.writer(fileObj)
            df = df.reset_index()  # make sure indexes pair with number of rows
            for index, row in df.iterrows():
                rows = (row['geoName'], row[text])
                writerObj.writerow(rows)
        edit.mousePressEvent = self.rightarea
        file_exists = exists("searches.csv")

        if file_exists == True:
            self.downarea(self)


if __name__ == '__main__':
    try:
        # show the app icon on the taskbar
        import ctypes
        myappid = 'yourcompany.yourproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    finally:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.setWindowFlags(window.windowFlags() &
                              QtCore.Qt.CustomizeWindowHint)
        window.setWindowFlags(window.windowFlags() & ~
                              QtCore.Qt.WindowMinMaxButtonsHint)
        window.show()
        sys.exit(app.exec())
