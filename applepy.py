import plotting_tools
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
from pathlib import Path
import numpy as np


def load_data(self):
    file_path = get_path(self)
    if file_path != "":
        data = get_data(file_path)
        if data is not None:
            self.filename = Path(file_path).name
            self.dataframe = data
            plot_selection(self)


def saveFileDialog(self, documenttype="Text file (*.txt)", title="Save file"):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    filename = f"{self.filename[:-4]}_{self.selection}.txt"
    fileName = QFileDialog.getSaveFileName(self, title, filename,
                                           documenttype, options=options)
    return fileName


def export_data(self):
    if self.filename is not None:
        path = saveFileDialog(self, title="Save selected data")
        filename = path[0]
        if filename[-4:] != ".txt":
            filename = filename + ".txt"

        xdata = self.dataframe["time"]
        if self.selection == "time_vs_ticks":
            ydata = list(range(len(xdata)))
        elif self.selection == "delay_second":
            ydata = []
            for i in range(len(xdata)):
                if i != len(xdata) - 1:
                    ydata.append(xdata[i] - xdata[i + 1] + 1)
                else:
                    ydata.append(0)
                i += 1
        elif self.selection == "delay_total":
            ydata = []
            for i in range(len(xdata)):
                ydata.append(xdata[i] - i - 2)
                i += 1
        else:
            ydata = self.dataframe[self.selection]

        array = np.stack([xdata, ydata], axis=1)
        np.savetxt(filename, array, delimiter="\t")


def plot_selection(self):
    if self.dataframe is not None:
        selection = get_selection(self)
        title = f"{selection} - {self.filename}"
        self.plot_figure(title=title, selection=selection)


def get_selection(self):
    selection = str(self.selected_item.currentText())
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
        self.type = "gas"
    elif selection == "Ar Flow (SCCM)":
        selection = "ar_flow"
        self.type = "gas"
    elif selection == "Delay per second":
        selection = "delay_second"
        self.type = "delay_second"
    elif selection == "Total delay":
        selection = "delay_total"
        self.type = "delay_total"
    elif selection == "Time vs ticks":
        selection = "time_vs_ticks"
        self.type = "ticks"
    elif selection == "Average delay (absolute)":
        selection = "average_delay_abs"
        self.type = "delay_second"
    elif selection == "Average delay":
        selection = "average_delay"
        self.type = "delay_second"
    else:
        self.type = "other"
        self.selection = "coil1_current"
    self.selection = selection
    return selection


def get_data(file_path):
    df = pd.read_csv(file_path, sep="\s+", decimal=",", skiprows=2)
    try:
        df.columns = ["time", "coil1_current", "coil2_current", "bias_voltage", "value3", "mdx2_current", "mdx2_power",
                      "mdx2_voltage", "mdx1_current", "value11", "value12", "value13", "value14", "value15", "value17",
                      "value18", "value16", "mdx1_power", "mdx1_voltage", "ar_flow", "n2_flow"]
    except ValueError:
        print("Could not read file, are you sure this is an Adam log?")
        df = None
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
