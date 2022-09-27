# CallUI.py
import sys
from PyQt5 import QtWidgets, uic
import plotting_tools
import applepy

Ui_MainWindow, QtBaseClass = uic.loadUiType("form.ui")


class CallUI(QtBaseClass, Ui_MainWindow):
    def __init__(self):
        QtBaseClass.__init__(self)
        Ui_MainWindow.__init__(self)
        self.dataframe = None
        self.filename = None
        self.figurecanvas = None
        self.type = None
        self.selection = None
        self.setupUi(self)
        self.connect_actions()
        applepy.load_empty(self)

    def connect_actions(self):
        self.load_data_button.clicked.connect(lambda: applepy.load_data(self))
        self.selected_item.activated.connect(lambda: applepy.plot_selection(self))
        self.export_button.clicked.connect(lambda: applepy.export_data(self))


    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def plot_figure(self, selection=None, layout=None, title=None):
        if title == None:
            title = self.get_title()
        if layout == None:
            layout = self.graphlayout
        self.clear_layout(layout)
        self.figurecanvas = plotting_tools.plotGraphOnCanvas(self, layout,
                                                             title=title, scale="linear", selection = selection)


    def get_title(self):
        if self.dataframe is None:
            title = ""
        else:
            title = self.filename
        return title

def setUpWindow():
    app = QtWidgets.QApplication(sys.argv)
    nowWindow = CallUI()
    nowWindow.showMaximized()
    sys.exit(app.exec_())
