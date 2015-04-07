import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from main_gui import Ui_Dialog as main_Ui

class MainDialog(QDialog):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.ui = main_Ui()
		self.ui.setupUi(self)
		self.XL_fileName = ""
		# self.setFixedSize(600,430)
		# self.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowCloseButtonHint )
		# self.validator = QtGui.QRegExpValidator(QtCore.QRegExp('[a-zA-Z\s]+'))
        #
		# self.delAction = QtGui.QAction("Delete Row", self)
		# self.delAction.setIcon(QtGui.QIcon("remove.png"))
		# self.previewAction = QtGui.QAction("Preview Door", self)
        #
		# self.popMenu = QtGui.QMenu(self)
		# self.popMenu.addAction(self.delAction)
        #
		# self.ui.doorList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		# self.ui.doorList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
		# self.ui.doorList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		# self.ui.doorList.setColumnWidth(1,50)
		# self.ui.doorList.setColumnWidth(2,65)
		# self.ui.doorList.setColumnWidth(3,65)
		# self.ui.doorList.setColumnWidth(4,75)
		# self.ui.doorList.setColumnWidth(5,165)
        #
		# self.connect(self.ui.doorList, QtCore.SIGNAL("customContextMenuRequested(const QPoint&)"), self.context_menu)
		# self.connect(self.ui.genButton, QtCore.SIGNAL("clicked()"), self.tacos)
		# self.connect(self.ui.importButton, QtCore.SIGNAL("clicked()"), self.import_xls)
		# self.connect(self.ui.addButton, QtCore.SIGNAL("clicked()"), self.add_door)
		# self.connect(self.ui.doorList, QtCore.SIGNAL("itemChanged (QTableWidgetItem*)"), self.data_edited)
		# self.connect(self.ui.configButton, QtCore.SIGNAL("clicked()"), self.config_menu)
		# self.connect(self.delAction, QtCore.SIGNAL("triggered (bool)"), self.remove_door)
		# self.ui.jobNameEdit.setValidator(self.validator)
		# self.ui.roomNameEdit.setValidator(self.validator)




if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = MainDialog()
    w.show()

    sys.exit(app.exec_())
