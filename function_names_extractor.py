import re
import os
import json
import pandas as pd
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from ast import literal_eval

import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QWidget):

    def __init__(self, data):
        super().__init__()
        self.title = 'Calling Order'
        self.left = 0
        self.top = 0
        self._data = data
        self.width = 800
        self.height = 600
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 

        # Show widget
        self.show()
        
    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.rowCount())
        self.tableWidget.setColumnCount(self.columnCount())
        
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.tableWidget.setItem(i,j, QTableWidgetItem(str(self._data.iloc[i][self._data.keys()[j]])))
        
        header = self.tableWidget
        for column in range(self.columnCount()):      
            header.setColumnWidth(column, 450)
        

        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class FunctionsIdentifier:
    
    def __init__(self):
        
        self.dirs_tree = []
        self.dirs_dict = {}
        self.ROOT = os.getcwd()

    def tree_constructor(self, s):
    
        if not os.path.isdir(s):
            return
        
        else:
            
            self.dirs_tree.append(s)
            list_dirs = [d for d in os.listdir(s) if os.path.isdir(s)]
            for directory in list_dirs:
                self.tree_constructor(f'{s}/{directory}')
            return
        

    def tree_constructor_caller(self):
            
        for dirs in os.listdir(self.ROOT): 
            if os.path.isdir(f"{self.ROOT}/{dirs}"):
                self.tree_constructor(f"{self.ROOT}/{dirs}")
        self.dirs_tree.append(self.ROOT)
        self.dirs_tree_final = [z for z in self.dirs_tree if re.match(r'((.*(__pycache__))|(.*(.git)))', z)==None]


    def dict_constructor(self):
        
        self.tree_constructor_caller()
        
        for direc in self.dirs_tree_final:
            dirs_dict_value = []
            for file in os.listdir(direc):
                file_value = {}
                if re.match(r'(.*(\.py))', file)!=None and re.match(r'(__init__.py)', file)==None:
                    with open(f'{direc}/{file}', 'r') as func:
                        f = func.read()
                        func.close()
                    r = re.findall(r'(def\s\w*\(\w.*\))', f)
                    file_value[file] = r
                    dirs_dict_value.append(file_value)
                self.dirs_dict[direc] = dirs_dict_value
        #print(self.dirs_dict.keys())


    def exporting(self):
        
        self.dict_constructor()
        
        with open(f'{self.ROOT}/directores_and_files.json', 'w') as f:
            json.dump(self.dirs_dict,f, indent=2)
            f.close()
            
        with open(f'{self.ROOT}/directores.json', 'w') as f:
            list_temp = [x for x in self.dirs_dict.keys()]
            json.dump(list_temp,f, indent=2)
            f.close()
            
    def printing_formatted_dataframe(self, df):
        
        """ app = QApplication(sys.argv)
        model = pandasModel(df)
        view = QTableView()
        view.setModel(model)
        view.resize(1300, 1000)
        view.show()
        sys.exit(app.exec_()) """
        
        app = QApplication(sys.argv)
        ex = App(df)
        sys.exit(app.exec_())
        
    def dataframe_generation(self):
               
        df = pd.DataFrame.from_dict(self.dirs_dict, orient='index').T.reset_index()
        temp = df['/home/christian/agropro']
        for i in temp.index:
            l = [*temp.iloc[i]]
            for j in l:
                print('')
                print(temp.iloc[i][j])
        #self.printing_formatted_dataframe(df)

        
if __name__ == '__main__':
    
    c = FunctionsIdentifier()
    c.exporting()
    #c.dataframe_generation()
    
    """ app = QApplication(sys.argv)
    model = pandasModel(df)
    view = QTableView()
    view.setModel(model)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_()) """
    
    """ app = QApplication(sys.argv)
    ex = App(df)
    sys.exit(app.exec_()) """