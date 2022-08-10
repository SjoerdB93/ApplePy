import plotting_tools
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
from pathlib import Path


def load_data(self):
    try:
        file_path = get_path(self)
        self.filename = Path(file_path).name
        data = get_data(file_path)
        self.dataframe = data
        plot_selection(self)
    except:
        pass

def plot_selection(self):
    if self.dataframe is not None:
        selection = str(self.selected_item.currentText())
        title = f"{selection} - {self.filename}"
        if selection == "Coil 1 current":
            selection = "coil1_current"
            self.type = "coil_current"
        elif selection == "Coil 2 current":
            selection = "coil2_current"
            self.type = "coil_current"
        elif selection == "Bias Voltage":
            selection = "bias_voltage"
            self.type = "voltage"
        elif selection == "Value 3":
            selection = "value3"
        elif selection == "MDX 2 Current":
            selection = "mdx2_current"
            self.type = "current"
        elif selection == "MDX 2 Voltage":
            selection = "mdx2_voltage"
            self.type = "voltage"
        elif selection == "MDX 2 Power":
            selection = "mdx2_power"
            self.type = "power"
        elif selection == "MDX 1 Power":
            selection = "mdx1_power"
            self.type = "power"
        elif selection == "MDX 1 Current":
            selection = "mdx1_current"
            self.type = "current"
        elif selection == "MDX 1 Voltage":
            selection = "mdx1_voltage"
            self.type = "voltage"
        elif selection == "N2 Flow (SCCM)":
            selection = "n2_flow"
            type = "gas"
        elif selection == "Ar Flow (SCCM)":
            selection = "ar_flow"
            type = "gas"
        elif selection == "Ticks":
            selection = "time"
            self.type = "ticks"
        else:
            selection = "coil1_current"
        self.plot_figure(title = title, selection=selection)


def get_data(file_path):
    df = pd.read_csv(file_path, sep="\s+", decimal=",", skiprows=2)
    df.columns = ["time", "coil1_current", "coil2_current", "bias_voltage", "value3", "mdx2_current", "mdx2_power",
                  "mdx2_voltage", "mdx1_current", "value11", "value12", "value13", "value14", "value15", "value17",
                  "value_18", "value16", "mdx1_power", "mdx1_voltage", "ar_flow", "n2_flow"]
    return df

def define_canvas(self):
    layout = self.graphlayout
    self.clear_layout(self.graphlayout)
    self.figurecanvas = plotting_tools.plotGraphOnCanvas(self, layout, scale="linear", marker=None)


def load_empty(self):
    canvas = plotting_tools.PlotWidget(xlabel="X value", ylabel="Y Value",
                                                    title="Plot")
    create_layout(self, canvas, self.graphlayout)


def create_layout(self, canvas, layout):
    toolbar = NavigationToolbar(canvas, self)
    layout.addWidget(canvas)
    layout.addWidget(toolbar)


def get_path(self, documenttype="Text file (*.txt);;All Files (*)"):
    dialog = QFileDialog
    options = dialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    path = QFileDialog.getOpenFileName(self, "Open files", "",
                                        documenttype, options=options)[0]
    return path
