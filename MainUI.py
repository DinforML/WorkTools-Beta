# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainPage(object):
    def setupUi(self, MainPage):
        MainPage.setObjectName("MainPage")
        MainPage.resize(311, 583)
        self.centralwidget = QtWidgets.QWidget(MainPage)
        self.centralwidget.setObjectName("centralwidget")
        self.sportFlow = QtWidgets.QCheckBox(self.centralwidget)
        self.sportFlow.setGeometry(QtCore.QRect(90, 100, 141, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.sportFlow.setFont(font)
        self.sportFlow.setObjectName("sportFlow")
        self.nsportFlow = QtWidgets.QCheckBox(self.centralwidget)
        self.nsportFlow.setGeometry(QtCore.QRect(90, 140, 141, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.nsportFlow.setFont(font)
        self.nsportFlow.setObjectName("nsportFlow")
        self.lastBetTime = QtWidgets.QCheckBox(self.centralwidget)
        self.lastBetTime.setGeometry(QtCore.QRect(90, 180, 141, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.lastBetTime.setFont(font)
        self.lastBetTime.setObjectName("lastBetTime")
        self.upamountTime = QtWidgets.QCheckBox(self.centralwidget)
        self.upamountTime.setGeometry(QtCore.QRect(90, 220, 171, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.upamountTime.setFont(font)
        self.upamountTime.setObjectName("upamountTime")
        self.parent = QtWidgets.QCheckBox(self.centralwidget)
        self.parent.setGeometry(QtCore.QRect(90, 260, 141, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.parent.setFont(font)
        self.parent.setObjectName("parent")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(50, 370, 231, 31))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.Author = QtWidgets.QLabel(self.centralwidget)
        self.Author.setGeometry(QtCore.QRect(240, 0, 71, 16))
        self.Author.setObjectName("Author")
        self.VersionText = QtWidgets.QLabel(self.centralwidget)
        self.VersionText.setGeometry(QtCore.QRect(0, 0, 101, 20))
        self.VersionText.setObjectName("VersionText")
        self.Logger = QtWidgets.QTextBrowser(self.centralwidget)
        self.Logger.setGeometry(QtCore.QRect(20, 410, 271, 141))
        self.Logger.setObjectName("Logger")
        self.fileButton = QtWidgets.QToolButton(self.centralwidget)
        self.fileButton.setGeometry(QtCore.QRect(230, 70, 41, 21))
        self.fileButton.setObjectName("fileButton")
        self.fileLabel = QtWidgets.QLabel(self.centralwidget)
        self.fileLabel.setGeometry(QtCore.QRect(30, 70, 61, 21))
        self.fileLabel.setObjectName("fielLabel")
        self.filePath = QtWidgets.QLabel(self.centralwidget)
        self.filePath.setGeometry(QtCore.QRect(90, 72, 131, 20))
        self.filePath.setObjectName("filePath")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(100, 310, 91, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        MainPage.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainPage)
        self.statusbar.setObjectName("statusbar")
        MainPage.setStatusBar(self.statusbar)

        self.retranslateUi(MainPage)
        QtCore.QMetaObject.connectSlotsByName(MainPage)

    def retranslateUi(self, MainPage):
        _translate = QtCore.QCoreApplication.translate
        MainPage.setWindowTitle(_translate("MainPage", "MainPage"))
        self.sportFlow.setText(_translate("MainPage", "体育流水"))
        self.nsportFlow.setText(_translate("MainPage", "娱乐流水"))
        self.lastBetTime.setText(_translate("MainPage", "最后投注时间"))
        self.upamountTime.setText(_translate("MainPage", "(代)充值次数 #历史"))
        self.parent.setText(_translate("MainPage", "上级代理"))
        self.Author.setText(_translate("MainPage", "Author：Din"))
        self.VersionText.setText(_translate("MainPage", "Version：1.0-beta"))
        self.fileButton.setText(_translate("MainPage", "导入"))
        self.fileLabel.setText(_translate("MainPage", "檔案位置："))
        self.filePath.setText(_translate("MainPage", "待导入....."))
        self.startButton.setText(_translate("MainPage", "查询"))
