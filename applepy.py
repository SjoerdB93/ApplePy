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
        self.dataframe = data
        if data is not None:
            self.filename = Path(file_path).name
            self.dataframe = data
            plot_selection(self)


def save_file_dialog(self, selection_left, selection_right, documenttype="Text file (*.txt)", title="Save file"):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog

    filename_suggested = self.filename[:-4]
    append = ""
    selections = [selection_left, selection_right]
    for value in selections:
        if value != "None":
            append += f"_{value}"

    filename_suggested += f"{append}.txt"
    filename = QFileDialog.getSaveFileName(self, title, filename_suggested,
                                           documenttype, options=options)
    return filename


def export_data(self):
    if self.filename is not None:
        time_dataframe = self.dataframe["time"]
        time = ["time"]
        time.extend(time_dataframe.values.tolist())

        selection_left = plotting_tools.get_ylabel_and_dfselection(get_selection(self, "left"))[1]
        selection_right = plotting_tools.get_ylabel_and_dfselection(get_selection(self, "right"))[1]

        path = save_file_dialog(self, selection_left, selection_right, "Save selected data")
        filename = path[0]
        if filename[:-4] != ".txt":
            filename += ".txt"
        ydata_left = [selection_left]
        ydata_right = [selection_right]
        if filename != "":
            if selection_left == "Time vs ticks" or selection_left == "Delay per second" or selection_left == "Total delay" \
                    or selection_left == "Average delay (absolute)" or selection_left == "Average delay":
                ydata_left.extend(get_y_data_for_time_operatons(self, selection_left))
            elif selection_left == "None":
                ydata_left = None
            else:
                ydata_left.extend(self.dataframe[selection_left])

            if selection_right == "Time vs ticks" or selection_right == "Delay per second" or \
                    selection_right == "Total delay" or selection_right == "Average delay (absolute)" \
                    or selection_right == "Average delay":
                ydata_right.extend(get_y_data_for_time_operatons(self, selection_right))
            elif selection_right == "None":
                ydata_right = None
            else:
                print(selection_right)
                ydata_right.extend(self.dataframe[selection_right])

            total_stack = []
            for value in [time, ydata_left, ydata_right]:
                if value is not None:
                    total_stack.append(value)

            array = np.stack(total_stack, axis=1)
            np.savetxt(filename, array, delimiter="\t", fmt="%s")


def get_y_data_for_time_operatons(self, selection):
    time = self.dataframe["time"]

    if selection == "Time vs ticks":
        y_data = list(range(len(time)))
    elif selection == "Delay per second":
        y_data = []
        for i in range(len(time)):
            if i != len(time) - 1:
                y_data.append(time[i + 1] - time[i] - 1)
            else:
                y_data.append(0)
            i += 1
    elif selection == "Total delay":
        y_data = []
        for i in range(len(time)):
            y_data.append(time[i] - i - 2)
            i += 1
    elif selection == "Average delay (absolute)":
        time_diff = []
        total_delay = 0
        y_data = []
        for i in range(len(time)):
            if i != len(time) - 1:
                time_diff.append(abs(time[i + 1] - time[i] - 1))
            else:
                time_diff.append(0)
            i += 1
        for i in range(len(time)):
            total_delay += time_diff[i]
            y_data.append(total_delay / (time[i] - time[0] + 1))
    elif selection == "Average delay":
        time_diff = []
        total_delay = 0
        y_data = []
        for i in range(len(time)):
            if i != len(time) - 1:
                time_diff.append(time[i + 1] - time[i] - 1)
            else:
                time_diff.append(0)
            i += 1
        for i in range(len(time)):
            total_delay += time_diff[i]
            y_data.append(total_delay / (time[i] - time[0] + 1))
    return y_data


def plot_selection(self):
    if self.dataframe is not None:
        selection_left = get_selection(self, "left")
        selection_right = get_selection(self, "right")
        if selection_right != "None" and selection_left != "None":
            title = f"{selection_left}, {selection_right} - {self.filename}"
        else:
            if selection_left == "None":
                title = f"{selection_right} - {self.filename}"
            elif selection_right == "None":
                title = f"{selection_left} - {self.filename}"
            else:
                title = "Plot"

        self.plot_figure(title=title, selection_left=selection_left, selection_right=selection_right)


def get_selection(self, axis):
    if axis == "left":
        selection = str(self.selected_item.currentText())
    if axis == "right":
        selection = str(self.selected_item_right.currentText())
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
