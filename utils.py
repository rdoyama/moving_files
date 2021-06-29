"""
Some useful and general method and classes
"""

from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QWidget,
			QHBoxLayout, QSizePolicy, QTextEdit)

from PyQt5.QtGui import QTextCursor

import random
import re
import os
import glob

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class About(object):
	def show(self, Widget, version, author, git):
		text = """
			<center>
			  <h2>Moving Files App</h2>
			  <br><b>Version:</b></br> {}
			  <br><b>Author:</b></br> {}
			  <br><b>Download </b></br> <a href="{}">here</a>
			</center>
		""".format(version, author, git)

		Widget.resize(250, 100)

		Widget.layout = QVBoxLayout()
		Widget.setWindowTitle("About")

		textLabel = QLabel(text)
		textLabel.setOpenExternalLinks(True)
		Widget.layout.addWidget(textLabel)
		Widget.setLayout(Widget.layout)


class Statistics(object):
	def create(self, Widget):
		text = """
			<br>Average: saushuhauhusdgyagsdasdgahg</br>
			<br>Other statistics</br>
		"""

		boxLayout = QVBoxLayout()

		self.textLabel = QLabel(text)
		boxLayout.addWidget(self.textLabel)
		Widget.setLayout(boxLayout)

	def update(self, data):
		new_text = """
			<br>Average: 123</br>
			<br>Other statistics123</br>
		"""
		self.textLabel.setText(new_text)


class Plots(object):
	def create(self, Widget):
		boxLayout = QHBoxLayout()
		self.leftPlot = PlotCanvas(plotType="bar")
		self.rightPlot = PlotCanvas(plotType="hist")
		boxLayout.addWidget(self.leftPlot)
		boxLayout.addWidget(self.rightPlot)
		Widget.setLayout(boxLayout)

	def update(self, data):
		self.leftPlot.plotBar(data)
		self.rightPlot.plotHist(data)


class LogBox(object):
	def create(self, Widget):
		boxLayout = QVBoxLayout()
		self.txtBrowser = QTextEdit()
		self.txtBrowser.setReadOnly(True)
		self.cursor = QTextCursor(self.txtBrowser.document())
		self.txtBrowser.setTextCursor(self.cursor)
		self.txtBrowser.append("Line 2")
		self.txtBrowser.append("Line 3")
		self.txtBrowser.append("Line 2")
		self.txtBrowser.append("Line 2")
		self.txtBrowser.append("Line 2")
		self.txtBrowser.append("Line 2")
		self.txtBrowser.moveCursor(QTextCursor.End)
		boxLayout.addWidget(self.txtBrowser)
		Widget.setLayout(boxLayout)

	def update(self, message):
		self.txtBrowser.append(message)


class PlotCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=3, dpi=100,
						data={}, plotType="hist"):
		fig = plt.Figure(figsize=(width, height), dpi=dpi)
		# fig.patch.set_alpha(0)
		fig.subplots_adjust(bottom=0.20, left=0.18)
		FigureCanvas.__init__(self, fig)
		self.setParent(parent)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

		if plotType == "hist":
			self.plotHist(data)
		elif plotType == "bar":
			self.plotBar(data)

	def plotHist(self, data):
		ax = self.figure.add_subplot(111)
		fileSizes = data.get("fileSizes", [])
		ax.hist(data, bins=min(len(fileSizes)//2 + 1, 30))
		ax.set_ylabel("File Count")
		ax.set_xlabel("Fize Size (kB)")
		ax.set_title("Histogram of file sizes")
		plt.tight_layout()
		self.draw()

	def plotBar(self, data, n=5):
		"""
		Plots the number of files moved in the last n runs
		"""
		# runStarts = data.get("runStarts", [])[-n:]
		runNumFiles = data.get("runNumFiles", [])[-n:]
		runCount = data.get("runCount", 0)
		runNo = list(range(max(runCount-n+1, 1), runCount+1))
		ax = self.figure.add_subplot(111)
		ax.bar(runNo, runNumFiles)
		# ax.set_xticks(runStarts)
		ax.set_ylabel("File Count")
		ax.set_xlabel("Run")
		ax.set_title(f"Files moved in the last {n} runs")
		# ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
		# ax.xaxis.set_tick_params(rotation=30)
		plt.tight_layout()
		self.draw()


def checkRegex(regex):
	try:
		re.compile(regex)
		return True
	except re.error:
		return False


def validPath(directory):
	return os.path.isdir(directory) and os.access(directory, os.W_OK)


def getValidFiles(srcDir, regex):
	allFinds = glob.glob(os.path.join(srcDir, "*"))
	matching = []
	for obj in allFinds:
		if re.match(regex, os.path.basename(obj)) is not None and\
					os.path.isfile(obj):
			matching.append(obj)
	return matching