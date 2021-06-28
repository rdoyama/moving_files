"""
Moving Files Application

While running, this application checks for files in a specified directory
that matches a regular expression and moves them to the output directory.
"""

import sys

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QTextCursor

from PyQt5.QtWidgets import (QApplication, QMainWindow,
	QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout,
	QStyleFactory, QGroupBox, QRadioButton, QCheckBox, QDialog,
	QFormLayout, QHBoxLayout, QSpinBox, QLabel, QStatusBar,
	QTextBrowser)

from utils import About, Statistics, Plots, Logs

__version__ = "1.0"
__author__ = "rdoyama"


class MoveFileAppUI(QMainWindow):
	"""
	Graphical User Interface class.

	First idea: one H layout on top for user input, timer
				one more below for one plot and statistics
				one last in the bottom for log

				plus: Menu, Help, status bar
	"""
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Moving Files App")
		# self.setFixedSize(1000, 600)
		self._createMenu()

		centralWidget = QWidget()
		self.mainLayout = QGridLayout()

		self.data = {
				"fileCount": 0,
				"runCount": 0,
				"runStarts": [],
				"runNumFiles": [],
				"fileSizes": [],
				"fileMoveTime": [],
				"fileMoveTimeTaken": []
		}

		self._createStatusBar()
		self._createInputsBox()
		self._createStatisticsBox()
		self._createPlotsBox()
		self._createLogBox()

		centralWidget.setLayout(self.mainLayout)
		self.setCentralWidget(centralWidget)

	def _createMenu(self):
		self.menu = self.menuBar().addMenu("&Menu")

		# Style submenu
		styleMenu = self.menu.addMenu("Style")
		styleOptions = {}
		for style in QStyleFactory.keys():
			styleMenu.addAction(style, lambda arg=style: self._changeStyle(arg))
		
		self.menu.addAction("&Exit", self.close)

		# Help menu
		self.help = self.menuBar().addMenu("&Help")
		self.help.addAction("About", self._aboutWindow)

	def _changeStyle(self, style):
		QApplication.setStyle(QStyleFactory.create(style))

	def _aboutWindow(self):
		widget = QDialog(self)
		about = About()
		about.show(widget, __version__,
					__author__,
					f"https://www.github.com/{__author__}/moving_files")
		widget.exec_()

	def _createStatusBar(self):
		self.statusBar = QStatusBar()
		self.statusBar.showMessage("Ready")
		self.setStatusBar(self.statusBar)

	def _createInputsBox(self):
		"""
		Location: Top left
		Reads user input: regex, dir, out_dir, timer
		"""
		boxLayout = QVBoxLayout()
		inputBox = QGroupBox("Inputs")
		inputBox.setLayout(boxLayout)

		##
		## Inputs
		formLayout = QFormLayout()

		self.regex = QLineEdit()
		self.regex.setAlignment(Qt.AlignRight)
		formLayout.addRow("Regex:", self.regex)

		self.sourceDir = QLineEdit()
		self.sourceDir.setAlignment(Qt.AlignRight)
		formLayout.addRow("Source Directory:", self.sourceDir)

		self.destDir = QLineEdit()
		self.destDir.setAlignment(Qt.AlignRight)
		formLayout.addRow("Destination Directory:", self.destDir)
		
		self.timer = QSpinBox(self)
		self.timer.setValue(60)
		self.timer.setMaximum(1000000)
		formLayout.addRow("Timer (seconds):", self.timer)

		boxLayout.addLayout(formLayout)

		##
		## Buttons + Timer
		buttonsLayout = QHBoxLayout()
		
		self.startButton = QPushButton("Start", self)
		self.stopButton = QPushButton("Stop", self)
		self.resetButton = QPushButton("Reset", self)
		buttonsLayout.addWidget(self.startButton)
		buttonsLayout.addWidget(self.stopButton)
		buttonsLayout.addWidget(self.resetButton)

		boxLayout.addLayout(buttonsLayout)

		self.mainLayout.addWidget(inputBox, 0, 0, 1, 1)

	def _createStatisticsBox(self):
		statsBox = QGroupBox("Statistics")
		self.stats = Statistics()
		self.stats.create(statsBox)
		# self.stats.update([]) # Replace with data

		self.mainLayout.addWidget(statsBox, 0, 1, 1, 1)

	def _createPlotsBox(self):
		plotsBox = QGroupBox("Plots")
		self.plots = Plots()
		self.plots.create(plotsBox)

		self.mainLayout.addWidget(plotsBox, 1, 0, 1, 2)

	def _createLogBox(self):
		logBox = QGroupBox("Log")
		self.logs = Logs()
		self.logs.create(logBox)
		# self.logs = QTextBrowser()
		# self.cursor = QTextCursor(self.logs.document())
		# self.logs.setTextCursor(self.cursor)
		# self.logs.setPlaceholderText("Enter some text here\nLine2")
		# # self.cursor.insertText("Line 1\nLine2")
		# self.logs.moveCursor(QTextCursor.End)

		# logBox.addWidget(self.logs)
		self.mainLayout.addWidget(logBox, 2, 0, 1, 2)


def main():
	app = QApplication([])
	gui = MoveFileAppUI()
	gui.show()

	sys.exit(app.exec_())


if __name__ == "__main__":
	main()