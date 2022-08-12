from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns

def plotGraphOnCanvas(self, layout, selection = None, title = "", scale="linear"):
    if self.type == "current":
        ylabel = "Current (mA)"
    elif self.type == "voltage":
        ylabel = "Voltage (V)"
    elif self.type == "coil_current":
        ylabel = "Current (A)"
    elif self.type == "gas":
        ylabel = "Gas flow (SCCM)"
    elif self.type == "power":
        ylabel = "Power (W)"
    elif self.type == "delay_total":
        ylabel = "Total delay (s)"
    elif self.type == "delay_second":
        ylabel = "Delay per second (s)"
    elif self.type == "ticks":
        ylabel = "Ticks"
    else:
        ylabel = "Value"
    canvas = PlotWidget(xlabel="Time (H:m:s)", ylabel=ylabel,
                        title = "Horizontal Scan")
    figure = canvas.figure
    data = self.dataframe
    plotgGraphFigure(data, canvas, selection = selection, filename=self.filename, title=title, scale=scale)
    layout.addWidget(canvas)
    dtFmt = mdates.DateFormatter('%H:%M:%S')
    if selection != "hh":
        figure.gca().xaxis.set_major_formatter(dtFmt)
    figurecanvas = [figure, canvas]
    self.toolbar = NavigationToolbar(canvas, self)
    layout.addWidget(self.toolbar)
    return figurecanvas

def plotgGraphFigure(df, canvas, selection = None, filename="", xlim=None, title="", scale="linear",marker=None,
                     linestyle="solid"):
    fig = canvas.theplot
    time = df["time"]
    t = pd.to_datetime(time, unit='s')  # convert to datetime

    if selection == "time_vs_ticks":
        ticks = list(range(len(time)))
        fig.plot(t, ticks, label=filename, linestyle=linestyle, marker=marker)
    elif selection == "delay_second":
        time_diff = []
        for i in range(len(time)):
            if i != len(time) - 1:
                time_diff.append(time[i] - time[i+1] + 1)
            else:
                time_diff.append(0)
            i += 1
        fig.plot(t, time_diff, label=filename, linestyle=linestyle, marker=marker)
    elif selection == "delay_total":
        time_diff = []
        for i in range(len(time)):
            time_diff.append(time[i] - i - 2)
            i += 1
        fig.plot(t, time_diff, label=filename, linestyle=linestyle, marker=marker)
    else:
        fig.plot(t, df[selection], label=filename, linestyle=linestyle, marker=marker)
    canvas.theplot.set_title(title)
    canvas.theplot.set_xlim(xlim)
    canvas.theplot.set_yscale(scale)



class PlotWidget(FigureCanvas):
    def __init__(self, parent=None, xlabel=None, ylabel='Intensity (arb. u)', title="", scale="linear"):
        super(PlotWidget, self).__init__(Figure())
        self.setParent(parent)
        sns.set_theme(style="whitegrid")
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.theplot = self.figure.add_subplot(111)
        self.theplot.set_title(title)
        self.theplot.set_xlabel(xlabel)
        self.theplot.set_ylabel(ylabel)
        self.figure.set_tight_layout(True)
        self.theplot.set_yscale(scale)