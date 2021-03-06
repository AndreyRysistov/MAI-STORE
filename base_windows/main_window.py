# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_files/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1126, 681)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.MainTab = QtWidgets.QTabWidget(self.centralwidget)
        self.MainTab.setEnabled(True)
        self.MainTab.setMinimumSize(QtCore.QSize(1104, 630))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(23, 7, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        self.MainTab.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.MainTab.setFont(font)
        self.MainTab.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.MainTab.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.MainTab.setToolTip("")
        self.MainTab.setStyleSheet("")
        self.MainTab.setDocumentMode(True)
        self.MainTab.setTabsClosable(False)
        self.MainTab.setMovable(False)
        self.MainTab.setTabBarAutoHide(False)
        self.MainTab.setObjectName("MainTab")
        self.productsTab = ProductsWidget()
        self.productsTab.setMinimumSize(QtCore.QSize(10, 10))
        self.productsTab.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.productsTab.setFont(font)
        self.productsTab.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.productsTab.setObjectName("productsTab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.productsTab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.MainTab.addTab(self.productsTab, "")
        self.suppliersTab = SuppliersWidget()
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.suppliersTab.setFont(font)
        self.suppliersTab.setObjectName("suppliersTab")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.suppliersTab)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.MainTab.addTab(self.suppliersTab, "")
        self.producersTab = ProducersWidget()
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.producersTab.setFont(font)
        self.producersTab.setObjectName("producersTab")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.producersTab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.MainTab.addTab(self.producersTab, "")
        self.storagesTab = StoragesWidget()
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.storagesTab.setFont(font)
        self.storagesTab.setObjectName("storagesTab")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.storagesTab)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.MainTab.addTab(self.storagesTab, "")
        self.deliveriesTab = DeliveriesWidget()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.deliveriesTab.setFont(font)
        self.deliveriesTab.setObjectName("deliveriesTab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.deliveriesTab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MainTab.addTab(self.deliveriesTab, "")
        self.accountingTab = AccountingWidget()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.accountingTab.setFont(font)
        self.accountingTab.setObjectName("accountingTab")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.accountingTab)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.MainTab.addTab(self.accountingTab, "")
        self.horizontalLayout_3.addWidget(self.MainTab)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.MainTab.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.MainTab.setWhatsThis(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Comic Sans MS\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.productsTab), _translate("MainWindow", "????????????"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.suppliersTab), _translate("MainWindow", "????????????????????"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.producersTab), _translate("MainWindow", "??????????????????????????"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.storagesTab), _translate("MainWindow", "????????????"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.deliveriesTab), _translate("MainWindow", "????????????????"))
        self.MainTab.setTabText(self.MainTab.indexOf(self.accountingTab), _translate("MainWindow", "????????"))
from windows.widgets.accounting import AccountingWidget
from windows.widgets.deliveries import DeliveriesWidget
from windows.widgets.producers import ProducersWidget
from windows.widgets.products import ProductsWidget
from windows.widgets.storages import StoragesWidget
from windows.widgets.suppliers import SuppliersWidget
