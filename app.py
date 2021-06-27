"""
Moving Files Application

While running, this application checks for files in a specified directory
that matches a regular expression and moves them to the output directory.
"""

import sys

from PyQt5.QtCore import QDateTime, Qt, QTimer

from PyQt5.QtWidgets import (QApplication, QMainWindow,
	QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout,
	QStyleFactory, QGroupBox, QRadioButton, QCheckBox, QDialog,
	QFormLayout, QHBoxLayout, QSpinBox, QLabel)

from utils import About, Statistics

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
		# self.setFixedSize(800, 600)
		self._createMenu()

		centralWidget = QWidget()
		self.mainLayout = QGridLayout()

		self._createInputsBox()
		self._createStatisticsBox()

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
					f"https://www.github.com/{__author__}")
		widget.exec_()

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
		stats = Statistics()
		stats.show(statsBox, [1, 2, 3, 4, 5]) # Replace with data

		self.mainLayout.addWidget(statsBox, 0, 1, 1, 1)


def main():
	app = QApplication([])
	gui = MoveFileAppUI()
	gui.show()

	sys.exit(app.exec_())


if __name__ == "__main__":
	main()