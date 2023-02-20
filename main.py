import os
import re
import sys
from collections import OrderedDict
from collections import namedtuple

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Signal, Qt, QSettings, QDir
from PySide6.QtGui import QAction, QPixmap, QColor
from PySide6.QtGui import QIcon, QTextCursor
from PySide6.QtWidgets import QFileDialog, QMenu, QMessageBox
from SiemensToolBox.SimaticDataTypes import s7Types
from SiemensToolBox.Step7V5.project import ProjectV5
from anytree import Node

from QtDesign import PlcLogCreator


class MyNode(Node):
    separator = "."


class PlclogConfigCreator(QtWidgets.QMainWindow, PlcLogCreator.Ui_MainWindow):
    newProjectSignal = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.project = None
        self.iconPath = self.resource_path(r"QtDesign\icon.ico")

        self.newProjectSignal.connect(self.newProject)
        self.newProjectSignal.connect(lambda: self.onSelectMPI(-1))
        self.newProjectSignal.connect(lambda: self.onSelectIp(-1))
        self.selectedSignals = []
        self.FastLogDB.setText("2700")
        self.setWindowIcon(QIcon(self.iconPath))
        self.setWindowTitle("PlcLog Creator")
        self.statusBar().show()

        self.treeView.AddSignals.connect(self.onAddSignal)

        self.plainTextEdit.customContextMenuRequested.connect(self._show_context_menu_TextEdit)
        self.plainTextEdit.cursorPositionChanged.connect(self.setReadOnly)

        self.pushButton_2.toggled.connect(self._change_context_menu)

        self.settings = QSettings()

        self.configText = ""
        self.version = "0.4"

    def _change_context_menu(self, state):
        if state:
            self.plainTextEdit.setContextMenuPolicy(Qt.DefaultContextMenu)
        else:
            self.plainTextEdit.setContextMenuPolicy(Qt.CustomContextMenu)

    def setReadOnly(self):
        coursor = self.plainTextEdit.textCursor()
        row = QTextCursor.blockNumber(coursor)
        if row > 1:
            self.plainTextEdit.setReadOnly(True)
        else:
            self.plainTextEdit.setReadOnly(False)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def onAbout(self):

        dlg = QMessageBox()
        dlg.setIconPixmap(QPixmap(self.iconPath))
        dlg.setWindowIcon(QIcon(self.iconPath))
        dlg.setWindowTitle("About PlcLog Config Creator")
        dlg.setText(f"""Step7 project reader to ease the selection of signals to be used by PlcLogger \n
        PlcLog-Creator Version {self.version}\n
        Created by Enese 2022""")

        dlg.show()
        dlg.exec()

    def onExport(self):

        fileDir = QFileDialog.getSaveFileName()[0]
        if fileDir != "":
            os.makedirs(fileDir, exist_ok=True)

            if self.checkBox.isChecked():
                awl = self.generateAwl()
                try:
                    with open(f"{fileDir}\\Fastlog.awl", 'w+') as f:
                        f.write(awl)
                except IOError:
                    raise

            cnf = self.generateConfig()
            try:
                with open(f"{fileDir}\\PlcLog.cnf", 'w+') as f:
                    f.write(cnf)
            except IOError:
                raise

    def onFastLogDbChange(self):
        self._drawTextEditField()

    def onFastLogSource(self, value):
        self._drawTextEditField()

    def onFastLogCheckbox(self):
        self._drawTextEditField()

    def newProject(self):

        self.project: ProjectV5
        self.selectedSignals = []
        self.plainTextEdit.clear()

        for station in self.project.stations.values():
            interfaces = station.getAllNetworkInterfaces()
            if len(interfaces) < 1:
                interfaces = list(self.project._networkInterfaces.values())

            tmpFolders = [module.subItems for module in station.modules if hasattr(module, "subItems")]

            folders = [val.blockOfflineFolder for sublist in tmpFolders for val in sublist]

            for folder in folders:
                self.comboBox_folder.addItem(folder.name, folder)

            for interface in interfaces:
                if interface.Type == s7Types.interface.IP:
                    self.comboBox_2.addItem(interface.Address, interface)
                elif interface.Type == s7Types.interface.MPI:
                    self.comboBox_3.addItem(f"MPI: {interface.Address}", interface)
                elif interface.Type == s7Types.interface.DP:
                    self.comboBox_3.addItem(f"DP: {interface.Address}", interface)

        location = self.project.projectPath
        if hasattr(self.project, "projectZipFile"):
            location = self.project.projectZipFile
        self.statusBar().showMessage(f"{self.project.projectName}: {location}")

    def onOpenProject(self, folder):
        settings = QSettings("PlcLog_Creator", "data")
        LastOpenFolder = settings.value("LastOpenFolder")
        dlg = QFileDialog()

        if LastOpenFolder:
            try:
                if QDir(LastOpenFolder).exists():
                    dlg.setDirectoryUrl(LastOpenFolder)
            finally:
                pass
        dlg.setNameFilter("Step7 projects (*.s7p *.zip)")

        if dlg.exec():
            file: str = dlg.selectedFiles()[0]
            settings.setValue("LastOpenFolder", dlg.directory().path())

            # if file.endswith(".s7p"):
            self.project = ProjectV5(file)
            self.project.loadProject()
            self.selectedSignals = None
            self.comboBox.clear()
            self.comboBox_2.clear()
            self.comboBox_3.clear()
            self.comboBox_folder.clear()

            self.newProjectSignal.emit()

    def onSelectedDB(self, index):
        if item := self.comboBox.itemData(index):
            data = item.layout.nodeTree
            self.treeView.modelData(data)


    def onSelectIp(self, ip):
        ip = self.comboBox_2.itemData(self.comboBox_2.currentIndex())
        if not ip: return
        text = self.configText.split("\n")
        rack = ip._parent.rack if ip._parent else 3

        if len(text) < 2:
            text[0] = f"#5;2"
            text.append(f"@{rack};{ip.Address}")
        else:
            text[1] = f"@{rack};{ip.Address}"

        self.configText = "\n".join(text)
        self._drawTextEditField()

    def onSelectMPI(self, mpi):
        mpi = self.comboBox_3.itemData(self.comboBox_3.currentIndex())
        if not mpi: return

        text = self.configText.split("\n")
        text[0] = f"#{mpi.Address};2"

        self.configText = "\n".join(text)
        self._drawTextEditField()

    def onSelectFolder(self, index):
        folder = self.comboBox_folder.itemData(index)
        if not folder: return

        blocks = sorted(folder.blockList.items(), key=lambda x: x[1].blockNumber)

        for key, value in blocks:  # folder.blockList.items():
            if key.startswith("DB"):
                self.comboBox.addItem(f"{value.blockType.name} {value.blockNumber}\t:{value.syblolName} ", value)
        self.comboBox.setCurrentIndex(0)

    def onAddSignal(self, signals):
        item = self.comboBox.itemData(self.comboBox.currentIndex())
        db = item.blockNumber

        rows = []
        YesAll = False

        for signal in signals:
            row = namedtuple("row", ["db", "adress", "name", "type", "dbSymbol"])
            row.db = db
            row.adress = signal.row_data.address
            row.name = signal.row_data.path
            row.type = signal.row_data.dataType
            row.dbSymbol = item.syblolName
            rows.append(row)

        for value in rows:
            name = value.name
            byte, bit = value.adress.split(".")
            _typeName = value.type
            if value.type == "REAL":

                _type = 2
                self.selectedSignals.append({"signal": value, "convert": False})

            elif value.type == "BOOL":
                _type = 1
                self.selectedSignals.append({"signal": value, "convert": False})
            elif YesAll:
                self.selectedSignals.append({"signal": value, "convert": True})

            else:
                msgBox = QMessageBox()
                msgBox.setWindowIcon(QIcon(self.iconPath))
                msgBox.setWindowTitle("PlcLog Creator Warning")
                msgBox.setText(f"Type {value.type} not valid for PLClog")

                prefixText1 = ""
                if not self.checkBox.checkState():
                    prefixText1 = "activate Fastlog, and "

                msgBox.setInformativeText(f"Do you want to {prefixText1}convert {value.name} to REAL in source")

                msgBox.setStandardButtons(
                    QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.No | QMessageBox.Cancel)
                msgBox.setDefaultButton(QMessageBox.Yes)
                ret = msgBox.exec()

                if ret == QMessageBox.YesAll:
                    self.checkBox.setChecked(True)
                    self.selectedSignals.append({"signal": value, "convert": True})
                    YesAll = True

                elif ret == QMessageBox.Yes:
                    self.checkBox.setChecked(True)
                    self.selectedSignals.append({"signal": value, "convert": True})
                elif ret == QMessageBox.Cancel:
                    break
                elif ret == QMessageBox.No:
                    self.selectedSignals.append({"signal": value, "convert": False})
        self._drawTextEditField()

    def _drawTextEditField(self):
        if self.pushButton_2.isChecked():
            text = self.generateAwl()
        else:
            text = self.generateConfig()
            self.configText = text

        self.plainTextEdit.clear()
        self.plainTextEdit.appendPlainText(text)

    def generateConfig(self):
        if self.checkBox.isChecked():
            return self.generateConfig_FastLogDB()

        # keep 2 first lines
        text = self.configText.split("\n")[:2]
        old = None

        if len(self.selectedSignals) > 0:

            addedVariables = []
            adress = 0
            for x in self.selectedSignals:
                signal, convert = x.values()
                listedname: list = signal.name.split(".")
                root = signal.dbSymbol if signal.dbSymbol != None else signal.db
                listedname.insert(0, root)
                name = ".".join(listedname)

                byte, bit = signal.adress.split(".")
                _typeName = signal.type
                _type = 2
                if signal.type == "BOOL":
                    _type = 1

                db = signal.db

                if self.checkBox.isChecked():
                    db = self.FastLogDB.text()

                    if ".".join(name.split(".")[:-1]) != old or _type == 2:
                        if adress % 8 != 0:
                            adress += (8 - (adress % 8))
                        if (adress // 8) % 2 != 0:
                            adress += 8
                        old = ".".join(name.split(".")[:-1])


                    byte = adress // 8
                    bit = adress % 8

                text.append(f"{name};{db};{byte};{_type};{bit}")

                adress += 32 if _type == 2 else 1
        return "\n".join(text)

    def generateConfig_FastLogDB(self):
        print("FastLog")
        text = self.configText.split("\n")[:2]

        if len(self.selectedSignals) == 0:
            return "\n".join(text)

        self.builVariableTable_awl(self.selectedSignals)
        db = self.FastLogDB.text()
        adress = 0
        old = None

        for node in self.root.leaves:
            path = ".".join([str(_.name) for _ in node.path][1:])
            _typeName = node.row_data
            _type = 2
            if node.row_data == "BOOL":
                _type = 1

            if ".".join(path.split(".")[:-1]) != old or _type == 2:
                if adress % 8 != 0:
                    adress += (8 - (adress % 8))
                if (adress // 8) % 2 != 0:
                    adress += 8
                old = ".".join(path.split(".")[:-1])
            byte = adress // 8
            bit = adress % 8
            text.append(f"{path};{db};{byte};{_type};{bit}")

            adress += 32 if _type == 2 else 1
        return "\n".join(text)

    def renameIfExist(self, variable, added=None):
        if added is None:
            added = []
        if variable in added:
            if ending := re.search(r"(.*)_(\d+)$", variable):
                new = self.renameIfExist(f"{ending[1]}_{int(ending[2]) + 1}", added)
            else:
                new = self.renameIfExist(f"{variable}_1", added)
            if len(new) > 24:
                new = self.renameIfExist(f"{ending[1][:-1]}_{int(ending[2]) + 1}", added)
            added.append(new)
            return new
        else:
            added.append(variable)
            return variable





    def buildDict(self, root, signals):
        rootname, signaltype = signals

        if rootname[0] not in root.keys():
            root[rootname[0]] = {}
        try:
            root[rootname[0]] = self.buildDict(root[rootname[0]], (rootname[1:], signaltype))
        except IndexError:
            root[rootname[0]] = signaltype
        return root


    def buildVariableTable_list(self, signals):
        _signals = []

        for x in signals:
            signal, convert = x.values()

            name: list = signal.name.split(".")
            root = signal.dbSymbol if signal.dbSymbol != None else signal.db
            root = root.replace(" ", "_")
            name.insert(0, root)
            newType = signal.type
            if convert:
                newType = "REAL"

            _signals.append((name, newType))
        return _signals

    def buildVariableTable_dict(self, signals):
        _signals = self.buildVariableTable_list(signals)
        dictSgnals = {}
        for listedName in _signals:
            self.buildDict(dictSgnals, listedName)
        self.sortVariableTable_dict(dictSgnals)
        return dictSgnals

    def sortVariableTable_dict(self, signals):
        sorted = OrderedDict(signals)
        root = MyNode("root")
        self.root = self.dictToNodeTree(sorted, root)
        return "a"






    def builVariableTable_awl(self, signals):
        dictSgnals = self.buildVariableTable_dict(signals)


        awl = ""
        awl += self.AwlGen(awl, dictSgnals)
        return awl

    def dictToNodeTree(self, signals: OrderedDict, root):



        for key, value in signals.items():
            if type(value) == dict:
                self.dictToNodeTree(value, MyNode(key, root))
            else:
                _node = MyNode(key, root)
                _node.__setattr__("row_data", value)
        return root



    def AwlGen(self, awl:str, dictSignals):
        for key, value in dictSignals.items():
            if type(value) == dict :
                awl += f"{key} : STRUCT\n"
                awl = self.AwlGen(awl, value)
                awl += "END_STRUCT ;\n"
                # return awl
            else:
                awl += f"{key}: {value} ;\n"

        return awl










    def generateAwl(self):

        awl = ""
        awl += f"FUNCTION_BLOCK FB {self.FastLogDB.text()}\n"
        awl += "TITLE = FastLog\n"
        awl += f"VERSION : {self.version}\n"
        awl += "\n"
        awl += "\n"
        awl += "VAR\n"



        # Build up Variables
        awl += self.builVariableTable_awl(self.selectedSignals)
        # addedVariables = []
        # for x in self.selectedSignals:
        #     signal, convert = x.values()
        #     name: str = signal.name.split(".")
        #     name = self.renameIfExist(name[-1], addedVariables)
        #
        #     name = name.replace("[", "")
        #     name = name.replace("]", "")
        #
        #     _type = "BOOL" if signal.type == "BOOL" else "REAL"
        #     awl += f"{name}: {_type} ;\n"

        awl += "END_VAR\n"
        awl += "\n"

        awl += "BEGIN\n"
        awl += "NETWORK\n"
        awl += "TITLE = Fastlog Signal Mapping\n"
        awl += "//Map signals from global Datablocks to this instance Datablock for fast logging\n"
        awl += "//Convertion of signals to format REAL (for PLClog)\n"
        awl += "\n"

        # Map signals and move to variables
        addedVariables = []
        for x in self.selectedSignals:
            signal, convert = x.values()
            listedname: list = signal.name.split(".")
            root = signal.dbSymbol if signal.dbSymbol != None else signal.db
            root = root.replace(" ", "_")
            listedname.insert(0, root)
            name = ".".join(listedname)
            # name: str = signal.name.split(".")
            # name = self.renameIfExist(name[-1], addedVariables)
            # name = name.replace("[", "")
            # name = name.replace("]", "")

            db = signal.db
            byte, bit = signal.adress.split(".")
            _type = signal.type

            if _type == "REAL":
                awl += f"L db{db}.dbd{byte};\n"
                awl += f"T #{name};\n"
                # awl += "\n"
            elif _type == "BOOL":
                awl += f"A db{db}.dbx{byte}.{bit};\n"
                awl += f"= #{name};\n"

            elif convert:
                if _type in ["INT", "WORD"]:
                    awl += f"L db{db}.dbw{byte};\n"
                    awl += "ITD;\n"
                    awl += "DTR;\n"
                    awl += f"T #{name};\n"
                    # awl += "\n"
                elif _type == "BYTE":
                    awl += f"L db{db}.dbb{byte};\n"
                    awl += "BTI;\n"
                    awl += "ITD;\n"
                    awl += "DTR;\n"
                    awl += f"T #{name};\n"
                    # awl += "\n"
                elif _type in ["DWORD", "DINT"]:
                    awl += f"L db{db}.dbd{byte};\n"
                    awl += "DTR;\n"
                    awl += f"T #{name};\n"
            else:
                awl += f"L db{db}.dbd{byte};\n"
                awl += f"T #{name};\n"
                awl += "\n"

            awl += "\n"
        awl += "END_FUNCTION_BLOCK"

        text = awl.split("\n")
        return "\n".join(text)

    def _show_context_menu_TextEdit(self, pos):
        if self.pushButton_2.isChecked():
            self.tableView.setContextMenuPolicy(Qt.DefaultContextMenu)

        coursor = self.plainTextEdit.cursorForPosition(pos)
        self.plainTextEdit.setTextCursor(coursor)
        row = QTextCursor.blockNumber(coursor)

        if row > 1:
            menu = QMenu()
            actionDelete = QAction(self)
            actionDelete.setText("Delete")
            #
            actionDeletaAll = QAction(self)
            actionDeletaAll.setText("Delete(All)")
            #
            menu.addAction(actionDelete)
            menu.addAction(actionDeletaAll)
            #
            fmt = QtGui.QTextCharFormat()
            fmt.setBackground(QColor('yellow'))
            coursor.movePosition(QTextCursor.StartOfBlock)
            coursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
            coursor.setCharFormat(fmt)
            #
            action = menu.exec(self.plainTextEdit.mapToGlobal(pos))

            fmt.setBackground(QColor('white'))
            coursor.setCharFormat(fmt)

            if action == actionDelete:
                self.selectedSignals.pop(row - 2)
            elif action == actionDeletaAll:
                self.selectedSignals = []

            if action:
                self._drawTextEditField()

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:

        if event.type() == QtCore.QEvent.MouseButtonDblClick and watched == self.treeView.viewport() and event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            self.treeView.addSignals()
            return True
        return super(PlclogConfigCreator, self).eventFilter(watched, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = PlclogConfigCreator()
    app.installEventFilter(widget)
    widget.show()

    sys.exit(app.exec())
