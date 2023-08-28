# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PlcLogCreator.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QSplitter, QVBoxLayout, QWidget)

from costumtreeview import CostumTreeView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 617)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSearch = QAction(MainWindow)
        self.actionSearch.setObjectName(u"actionSearch")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label)

        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout.addWidget(self.comboBox_2)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.comboBox_folder = QComboBox(self.centralwidget)
        self.comboBox_folder.setObjectName(u"comboBox_folder")

        self.gridLayout.addWidget(self.comboBox_folder, 0, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.comboBox_3 = QComboBox(self.centralwidget)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.horizontalLayout_2.addWidget(self.comboBox_3)


        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 1, 1, 1, 1)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.plainTextEdit = QPlainTextEdit(self.splitter)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setEnabled(True)
        self.plainTextEdit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.splitter.addWidget(self.plainTextEdit)
        self.treeView = CostumTreeView(self.splitter)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.treeView.setStyleSheet(u"alternate-background-color: #deefff; background-color: #ffffff;")
        self.treeView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.treeView.setAlternatingRowColors(False)
        self.treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.treeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.splitter.addWidget(self.treeView)

        self.gridLayout.addWidget(self.splitter, 2, 0, 1, 2)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkBox = QCheckBox(self.groupBox)
        self.checkBox.setObjectName(u"checkBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy1)
        self.checkBox.setMinimumSize(QSize(1, 17))

        self.verticalLayout.addWidget(self.checkBox)

        self.checkBox_RemPrefix = QCheckBox(self.groupBox)
        self.checkBox_RemPrefix.setObjectName(u"checkBox_RemPrefix")

        self.verticalLayout.addWidget(self.checkBox_RemPrefix)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.FastLogDB = QLineEdit(self.groupBox)
        self.FastLogDB.setObjectName(u"FastLogDB")

        self.horizontalLayout_3.addWidget(self.FastLogDB)

        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.horizontalLayout_3.setStretch(2, 1)
        self.horizontalLayout_3.setStretch(4, 1)

        self.gridLayout.addWidget(self.groupBox, 3, 0, 1, 2)

        self.gridLayout.setRowStretch(2, 5)
        self.gridLayout.setColumnStretch(0, 5)
        self.gridLayout.setColumnStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuOpen = QMenu(self.menubar)
        self.menuOpen.setObjectName(u"menuOpen")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuOpen.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuOpen.addAction(self.actionOpen)
        self.menuOpen.addAction(self.actionSearch)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)
        self.actionOpen.triggered.connect(MainWindow.onOpenProject)
        self.comboBox.currentIndexChanged.connect(MainWindow.onSelectedDB)
        self.comboBox_2.currentIndexChanged.connect(MainWindow.onSelectIp)
        self.comboBox_3.currentIndexChanged.connect(MainWindow.onSelectMPI)
        self.comboBox_folder.currentIndexChanged.connect(MainWindow.onSelectFolder)
        self.checkBox.stateChanged.connect(MainWindow.onFastLogCheckbox)
        self.pushButton_2.toggled.connect(MainWindow.onFastLogSource)
        self.FastLogDB.editingFinished.connect(MainWindow.onFastLogDbChange)
        self.pushButton.clicked["bool"].connect(MainWindow.onExport)
        self.actionAbout.triggered.connect(MainWindow.onAbout)
        self.checkBox_RemPrefix.stateChanged.connect(MainWindow.onRemove_prefix)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSearch.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"IP   ", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"MPI", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Config", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Fast Log", None))
        self.checkBox_RemPrefix.setText(QCoreApplication.translate("MainWindow", u"Remove Prefix", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"DB", None))
        self.FastLogDB.setText(QCoreApplication.translate("MainWindow", u"2700", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Show AWL Source", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.menuOpen.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

