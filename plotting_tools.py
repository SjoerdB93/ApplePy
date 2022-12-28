from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import applepy


# import seaborn as sns
def get_ylabel_and_dfselection(selection):
    if selection == "Coil 1 current":
        ylabel = "Current (A)"
        df_selection = "coil1_current"
    elif selection == "Coil 2 current":
        ylabel = "Current (A)"
        df_selection = "coil2_current"
    elif selection == "Bias Voltage":
        ylabel = "Voltage (V)"
        df_selection = "bias_voltage"
    elif selection == "MDX 1 Voltage":
        ylabel = "Voltage (V)"
        df_selection = "mdx1_voltage"
    elif selection == "MDX 2 Voltage":
        ylabel = "Voltage (V)"
        df_selection = "mdx2_voltage"
        df_selection = "mdx2_voltage"
    elif selection == "MDX 1 Current":
        ylabel = "Magnetron current (mA)"
        df_selection = "mdx1_current"
    elif selection == "MDX 1 Current":
        ylabel = "Magnetron current (mA)"
        df_selection = "mdx1_current"
    elif selection == "MDX 2 Current":
        ylabel = "Magnetron current (mA)"
        df_selection = "mdx2_current"
    elif selection == "Ar Flow (SCCM)":
        ylabel = "Gas flow (SCCM)"
        df_selection = "ar_flow"
    elif selection == "N2 Flow (SCCM)":
        ylabel = "Gas flow (SCCM)"
        df_selection = "n2_flow"
    elif selection == "MDX 2 Power":
        ylabel = "Magnetron power (W)"
        df_selection = "mdx2_power"
    elif selection == "MDX 1 Power":
        ylabel = "Magnetron power (W)"
        df_selection = "mdx1_power"
    elif selection == "Total delay":
        ylabel = "Total delay (s)"
        df_selection = selection
    elif selection == "Delay per second":
        ylabel = "Delay per second (s)"
        df_selection = selection
    elif selection == "Average delay" or selection == "Average delay (absolute)":
        ylabel = "Average delay (s)"
        df_selection = selection
    elif selection == "Time vs ticks":
        ylabel = "Ticks"
        df_selection = selection
    elif selection == "value11":
        ylabel = "Value"
        df_selection = selection
    elif selection == "value12":
        ylabel = "Value"
        df_selection =selection
    elif selection == "value13":
        ylabel = "Value"
        df_selection =selection
    elif selection == "value14":
        ylabel = "Value"
        df_selection =selection
    elif selection == "value15":
        ylabel = "Value"
        df_selection =selection
    elif selection == "value16":
        ylabel = "Value"
        df_selection =selection
    elif selection == "value17":
        ylabel = "Value"
        df_selection =selection
    elif selection == "value18":
        ylabel = "Value"
        df_selection = selection
    else:
        ylabel = ""
        df_selection = "None"
    return ylabel, df_selection


def plotGraphOnCanvas(self, layout, selection_left=None, selection_right=None, title="", scale="linear"):
    canvas = PlotWidget(xlabel="Time (H:m:s)")
    figure = canvas.figure
    data = self.dataframe
    plotgGraphFigure(self, data, canvas, selection_left=selection_left, selection_right=selection_right,
                     filename=self.filename, xlim = None, title=title, scale=scale)
    layout.addWidget(canvas)
    dtFmt = mdates.DateFormatter('%H:%M:%S')
    figure.gca().xaxis.set_major_formatter(dtFmt)
    figurecanvas = [figure, canvas]
    self.toolbar = NavigationToolbar(canvas, self)
    layout.addWidget(self.toolbar)
    return figurecanvas


def plotgGraphFigure(self, df, canvas, selection_left=None, selection_right=None, filename="", xlim=None, title="",
                     scale="linear", marker=None,
                     linestyle="solid"):
    axis = "left"
    plot_selection(self, canvas, df, selection_left, filename, marker, linestyle, axis, left = True)
    axis = "right"
    plot_selection(self, canvas, df, selection_right, filename, marker, linestyle, axis, left = False)
    fig = canvas.ax
    ylabel_right, selection = get_ylabel_and_dfselection(selection_right)
    ylabel_left, selection = get_ylabel_and_dfselection(selection_left)
    if not self.seperate_axes.isChecked():
        fig.set_ylabel(f"{ylabel_left}, {ylabel_right}")
    canvas.ax.set_title(title)
    canvas.ax.set_xlim(xlim)
    canvas.ax.set_yscale(scale)


def plot_selection(self, canvas, df, selection, filename, marker, linestyle, axis, left):

    fig1 = canvas.ax
    fig2 = canvas.ax
    time = df["time"]
    t = pd.to_datetime(time, unit='s')  # convert to datetime
    if axis == "left":
        fig = fig1
        ylabel, selection = get_ylabel_and_dfselection(selection)
        color = "#1f77b4"
        fig1.set_ylabel(ylabel)
    if axis == "right":
        if self.seperate_axes.isChecked():
            fig = fig1.twinx()
            fig2 = fig
        else:
            fig = fig2
        color = "#ff7f0e"
        ylabel, selection = get_ylabel_and_dfselection(selection)
        fig2.set_ylabel(ylabel)
    if selection == "None":
        fig.plot(label=filename)
    elif selection == "Time vs ticks" or selection == "Delay per second" or selection == "Total delay" or\
            selection == "Average delay (absolute)" or selection == "Average delay":
        y_data = applepy.get_y_data_for_time_operatons(self,selection)
        fig.plot(t, y_data, label=selection, linestyle=linestyle, marker=marker, color=color)
    else:
        fig.plot(t, df[selection], label=selection, linestyle=linestyle, marker=marker, color=color)

    h1, l1 = fig1.get_legend_handles_labels()
    h2, l2 = fig2.get_legend_handles_labels()
    if self.seperate_axes.isChecked() and not left:
        legend = fig1.legend(h1 + h2, l1 + l2, frameon = True, facecolor='white', framealpha=0.8)
        legend.remove()
        fig.add_artist(legend)
    if not self.seperate_axes.isChecked() and not left:
        legend = fig1.legend(h2, l2, frameon = True, facecolor='white', framealpha=0.8)
        legend.remove()
        fig.add_artist(legend)



class PlotWidget(FigureCanvas):
    def __init__(self, parent=None, xlabel="", ylabel="", title="", scale="linear"):
        plt.style.use('seaborn-whitegrid')
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title(title)
        self.figure.set_tight_layout(True)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        super(PlotWidget, self).__init__(self.figure)

