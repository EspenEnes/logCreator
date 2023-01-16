import typing

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QTreeView, QMenu,QAbstractItemView
from anytree import Node





class CostumTreeView(QTreeView):
    AddSignals = Signal(list)
    def __init__(self, parent):
        super(CostumTreeView, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.showActual = False


    def modelData(self, data):
        self.model1 = TreeDataModel(data)
        self.model2 = TableDataModel(data)
        self.setModel(self.model1)

    def addSignals(self):
        signals = []
        for x in self.selectedIndexes():
            if x.internalPointer().leaves and x.column() == 0:
                signals += x.internalPointer().leaves
                continue
            else:
                signals.append(x.internalPointer())

        self.AddSignals.emit([x for x in set(signals) if hasattr(x, "row_data")])

    def contextMenuEvent(self, arg__1) -> None:
        menu = QMenu()

        actionAddSignal = QAction(self)
        actionAddSignal.setText("Add Signal")
        menu.addAction(actionAddSignal)
        menu.addSeparator()
        actionListView= QAction(self)
        actionListView.setText("ListView")
        menu.addAction(actionListView)
        actionTreeView = QAction(self)
        actionTreeView.setText("TreeView")
        menu.addAction(actionTreeView)
        menu.addSeparator()
        actionshowActual = QAction(self)
        actionshowActual.setText("showActual")
        menu.addAction(actionshowActual)

        if action := menu.exec(self.mapToGlobal(arg__1.pos())):
            if action.text() == "ListView":

                self.setModel(self.model2)
                self.reset()
            elif action.text() == "TreeView":
                self.setModel(self.model1)
                self.reset()
            elif action.text() == "Add Signal":
               self.addSignals()
            elif action.text() == "showActual":
                self.model2.beginInsertColumns(QModelIndex(), 4,4)
                self.model2.showActual = True
                self.model2.endInsertColumns()





class TableDataModel(QAbstractItemModel):
    def __init__(self, data):
        super(TableDataModel, self).__init__()
        self.root = data.leaves
        self.showActual = False

    def columnCount(self, parent: QModelIndex = ...) -> int:
        """Returns the number of columns for the children of the given parent"""
        if self.showActual:
            return 4
        return 3

    def rowCount(self, parent: QModelIndex = ...) -> int:
        """Returns the number of rows under the given parent. When the parent is valid it means that rowCount is returning the number of children of parent.
        Note: When implementing a table based model, rowCount() should return 0 when the parent is valid."""
        if parent.isValid():
            return 0
        return len(self.root)


    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        """Returns the index of the item in the model specified by the given row, column and parent index.
        When reimplementing this function in a subclass, call createIndex() to generate model indexes that other components can use to refer to items in your model."""
        if parent.isValid():
            return QModelIndex()
        return QtCore.QAbstractItemModel.createIndex(self, row, column, self.root[row])

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        """Returns the data stored under the given role for the item referred to by the index."""
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return index.internalPointer().row_data.path
            elif index.column() == 1:
                return index.internalPointer().row_data.address
            elif index.column() == 2:
                return index.internalPointer().row_data.dataType

        if role == Qt.ItemDataRole.BackgroundRole:
            if index.row() % 2 == 0:
                return QtGui.QColor("light blue")

    def parent(self, child: QModelIndex) -> QModelIndex:
        """Returns the parent of the model item with the given index. If the item has no parent, an invalid QModelIndex is returned."""
        return QModelIndex()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section == 0:
                return "Name"
            elif section == 1:
                return "Address"
            elif section == 2:
                return "Type"
        return None

class TreeDataModel(QAbstractItemModel):

    def __init__(self, data):
        super(TreeDataModel, self).__init__()
        self.root = data
        self.showActual = False



    def columnCount(self, parent: QModelIndex = ...) -> int:
        """Returns the number of columns for the children of the given parent"""
        if self.showActual:
            return 4
        return 3

    def rowCount(self, parent: QModelIndex = ...) -> int:
        """Returns the number of rows under the given parent. When the parent is valid it means that rowCount is returning the number of children of parent.
        Note: When implementing a table based model, rowCount() should return 0 when the parent is valid."""
        if parent.isValid():
            return len(parent.internalPointer().children)
        return len(self.root.children)


    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        """Returns the data stored under the given role for the item referred to by the index."""
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return index.internalPointer().name
            elif index.column() == 1:
                if hasattr(index.internalPointer(), "row_data"):
                    return index.internalPointer().row_data.address
                else:
                    start = int(index.internalPointer().leaves[0].row_data.address.split(".")[0])
                    end = int(index.internalPointer().leaves[-1].row_data.address.split(".")[0])
                    return f"{start}..{end}"
            elif index.column() == 2:
                if hasattr(index.internalPointer(), "row_data"):
                    return index.internalPointer().row_data.dataType
                #todo Legg til hvilken type data er en parent (UDT, STRUCT, ARRAY), må gjøre endringer i Simatic
        elif role == Qt.ItemDataRole.FontRole:
            if not hasattr(index.internalPointer(), "row_data"):
                font = QtGui.QFont()
                font.setBold(True)
                return font


        if role == Qt.ItemDataRole.BackgroundRole:
            if index.row() % 2 == 0:
                return QtGui.QColor("light blue")

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        """Returns the index of the item in the model specified by the given row, column and parent index.
        When reimplementing this function in a subclass, call createIndex() to generate model indexes that other components can use to refer to items in your model."""
        if parent.isValid():
            return QtCore.QAbstractItemModel.createIndex(self, row, column, parent.internalPointer().children[row])
        return QtCore.QAbstractItemModel.createIndex(self, row, column, self.root.children[row])


    def parent(self, child: QModelIndex) -> QModelIndex:
        """Returns the parent of the model item with the given index. If the item has no parent, an invalid QModelIndex is returned."""

        if parent := child.internalPointer().parent:
            try:
                index = list.index([id(x) for x in parent.path[-2].children], id(parent))
                return QtCore.QAbstractItemModel.createIndex(self, index, 0, parent)
            except IndexError:
                return QModelIndex()
        return QModelIndex()

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> typing.Any:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section == 0:
                return "Name"
            elif section == 1:
                return "Address"
            elif section == 2:
                return "Type"
        return None