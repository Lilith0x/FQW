# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(540, 800)
        MainWindow.setMinimumSize(QtCore.QSize(540, 800))
        MainWindow.setMaximumSize(QtCore.QSize(540, 800))
        MainWindow.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resours/funko-pop-russia-Naruto-Shippuden-Naruto-Sexy-Jutsu-Box-Lunch-FU47079-.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("")
        MainWindow.setIconSize(QtCore.QSize(0, 0))
        MainWindow.setAnimated(False)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet("border-color: rgb(73, 77, 78);\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, -1, 551, 821))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tabWidget.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tabWidget.setAcceptDrops(False)
        self.tabWidget.setToolTipDuration(-1)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("color: rgb(255, 215, 0);\n"
"background-color: rgb(73, 77, 78);\n"
"\n"
"\n"
"")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setAutoFillBackground(False)
        self.tab_1.setStyleSheet("background-color: rgb(73, 77, 78);\n"
"border-color: rgb(255, 0, 0);\n"
"alternate-background-color: rgb(255, 0, 0);\n"
"\n"
"\n"
"")
        self.tab_1.setObjectName("tab_1")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_1)
        self.textBrowser.setGeometry(QtCore.QRect(6, 15, 500, 691))
        self.textBrowser.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.textBrowser.setStyleSheet("color:rgb(255, 215, 0);\n"
"background-color: rgb(73, 77, 78);\n"
"")
        self.textBrowser.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser.setObjectName("textBrowser")
        self.frame = QtWidgets.QFrame(self.tab_1)
        self.frame.setGeometry(QtCore.QRect(6, 720, 501, 71))
        self.frame.setStyleSheet("background-color: rgb(128, 128, 128);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 381, 71))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.textEdit.setFont(font)
        self.textEdit.setTabletTracking(True)
        self.textEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setStyleSheet("background-color: rgb(128, 128, 128);")
        self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit.setLineWidth(0)
        self.textEdit.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.textEdit.setAcceptRichText(True)
        self.textEdit.setCursorWidth(1)
        self.textEdit.setObjectName("textEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 0, 60, 70))
        self.pushButton_2.setTabletTracking(False)
        self.pushButton_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pushButton_2.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.pushButton_2.setAcceptDrops(False)
        self.pushButton_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_2.setStyleSheet("background-color: rgb(73, 77, 78);\n"
"color: rgb(255, 215, 0);")
        self.pushButton_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resours/micro.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(60, 60))
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setChecked(False)
        self.pushButton_2.setAutoRepeat(False)
        self.pushButton_2.setAutoExclusive(False)
        self.pushButton_2.setAutoRepeatDelay(300)
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setDefault(False)
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(380, 0, 60, 70))
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton.setStyleSheet("background-color: rgb(73, 77, 78);\n"
"color: rgb(255, 215, 0);")
        self.pushButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("resours/strelka.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon2)
        self.pushButton.setIconSize(QtCore.QSize(60, 60))
        self.pushButton.setCheckable(False)
        self.pushButton.setChecked(False)
        self.pushButton.setAutoRepeat(False)
        self.pushButton.setAutoExclusive(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("pushButton")
        self.frame.raise_()
        self.textBrowser.raise_()
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setAutoFillBackground(False)
        self.tab_2.setStyleSheet("background-color: rgb(73, 77, 78);\n"
"")
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.radioButton = QtWidgets.QRadioButton(self.tab)
        self.radioButton.setGeometry(QtCore.QRect(130, 320, 18, 18))
        self.radioButton.setText("")
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.tab)
        self.radioButton_2.setGeometry(QtCore.QRect(380, 320, 18, 18))
        self.radioButton_2.setText("")
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.tab)
        self.radioButton_3.setGeometry(QtCore.QRect(130, 660, 18, 18))
        self.radioButton_3.setText("")
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.tab)
        self.radioButton_4.setGeometry(QtCore.QRect(380, 660, 18, 18))
        self.radioButton_4.setText("")
        self.radioButton_4.setObjectName("radioButton_4")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(270, 370, 230, 280))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("resours/коробки/pngwin111111111g.com (4).png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(20, 370, 230, 280))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("resours/коробки/pwertwfngwing.com (1).png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(270, 30, 230, 280))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("resours/коробки/pngwinaeeg.com (3).png"))
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(20, 30, 230, 280))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("resours/коробки/p111111ngwing.com.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.tab)
        self.buttonBox.setGeometry(QtCore.QRect(155, 710, 211, 61))
        self.buttonBox.setSizeIncrement(QtCore.QSize(0, 0))
        self.buttonBox.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.tabWidget.addTab(self.tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.actiondffgf = QtWidgets.QAction(MainWindow)
        self.actiondffgf.setObjectName("actiondffgf")
        self.actiondfgd = QtWidgets.QAction(MainWindow)
        self.actiondfgd.setObjectName("actiondfgd")
        self.actionfg = QtWidgets.QAction(MainWindow)
        self.actionfg.setObjectName("actionfg")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AICA"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Введите ваш запрос..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Разговор"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Настройки"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Аватар"))
        self.actiondffgf.setText(_translate("MainWindow", "dffgf"))
        self.actiondfgd.setText(_translate("MainWindow", "dfgd"))
        self.actionfg.setText(_translate("MainWindow", "fg"))
