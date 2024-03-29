"""
Moving Files Application

While running, this application checks for files in a specified directory
that matches a regular expression and moves them to the output directory.
"""

import sys
import os
import time
import json

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QTextCursor

from PyQt5.QtWidgets import (QApplication, QMainWindow,
	QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout,
	QStyleFactory, QGroupBox, QRadioButton, QCheckBox, QDialog,
	QFormLayout, QHBoxLayout, QSpinBox, QLabel, QStatusBar,
	QTextBrowser, QCheckBox)

from utils import (About, Statistics, Plots, LogBox, checkRegex,
	validPath, getValidFiles)

__version__ = "1.0"
__author__ = "rdoyama"


class MoveFileAppUI(QMainWindow):
	"""
	Graphical User Interface class.

	Creates a simple menu, status bar and four boxes for:
	inputs, statistics, plots and logs. Actions, input
	checking, etc. is performed by the Controller class.
	"""
	def __init__(self, config):
		super().__init__()

		self.config = config

		self.setWindowTitle("Moving Files App")
		w = self.config["display"]["initialWidth"]
		h = self.config["display"]["initialHeight"]
		self.resize(w, h)
		self._createMenu()

		centralWidget = QWidget()
		self.mainLayout = QGridLayout()

		self._createStatusBar()
		self._createInputsBox()
		self._createStatisticsBox()
		self._createPlotsBox()
		self._createLogBox()

		centralWidget.setLayout(self.mainLayout)
		self.setCentralWidget(centralWidget)

	def _createMenu(self):
		self.menu = self.menuBar().addMenu("Menu")

		# Style submenu
		styleMenu = self.menu.addMenu("Style")
		styleOptions = {}
		for style in QStyleFactory.keys():
			styleMenu.addAction(style, lambda arg=style: self._changeStyle(arg))
		
		self.clearMenu = self.menu.addAction("Clear")

		self.menu.addAction("&Exit", self.close, shortcut="Ctrl+Q")

		# Help menu
		self.help = self.menuBar().addMenu("Help")
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
		Reads user input: Regex, Source dir, Destination dir and gives the
		option to overwrite existing files in the destination directory.
		"""
		boxLayout = QVBoxLayout()
		inputBox = QGroupBox("Inputs")
		inputBox.setLayout(boxLayout)

		##
		## Inputs
		formLayout = QFormLayout()

		self.regex = QLineEdit()
		self.regex.setAlignment(Qt.AlignRight)
		txtExample = "Example: for all .zip files use .*\.zip"
		self.regex.setPlaceholderText(txtExample)
		formLayout.addRow("Regex:", self.regex)

		self.sourceDir = QLineEdit()
		self.sourceDir.setAlignment(Qt.AlignRight)
		txtExample = "/home/user/source_dir"
		self.sourceDir.setPlaceholderText(txtExample)
		formLayout.addRow("Source Directory:", self.sourceDir)

		self.destDir = QLineEdit()
		self.destDir.setAlignment(Qt.AlignRight)
		txtExample = "/home/user/destination_dir"
		self.destDir.setPlaceholderText(txtExample)
		formLayout.addRow("Destination Directory:", self.destDir)
		
		##
		## Timer
		self.timer = QSpinBox(self)
		defaultValue = self.config["spin"]["defaultValue"]
		minValue = self.config["spin"]["minValue"]
		maxValue = self.config["spin"]["maxValue"]
		self.timer.setValue(defaultValue)
		self.timer.setMaximum(maxValue)
		self.timer.setMinimum(minValue)
		self.timer.setAlignment(Qt.AlignRight)
		formLayout.addRow("Timer (seconds):", self.timer)

		boxLayout.addLayout(formLayout)

		##
		## Buttons
		buttonsLayout = QHBoxLayout()
		
		self.startButton = QPushButton("Start", self)
		self.stopButton = QPushButton("Stop", self)
		self.resetButton = QPushButton("Reset", self)
		self.overwriteCheck = QCheckBox("Overwrite existing files", self)
		self.overwrite = False
		self.overwriteCheck.stateChanged.connect(self._checkOverwrite)

		buttonsLayout.addWidget(self.startButton)
		buttonsLayout.addWidget(self.stopButton)
		buttonsLayout.addWidget(self.resetButton)
		buttonsLayout.addWidget(self.overwriteCheck)

		boxLayout.addLayout(buttonsLayout)

		# self.regex.setText(".*jpg")
		# self.sourceDir.setText("/home/rafael/Desktop/teste/folder1")
		# self.destDir.setText("/home/rafael/Desktop/teste/folder2")
		# self.timer.setValue(4)

		self.mainLayout.addWidget(inputBox, 0, 0, 1, 7)

	def _checkOverwrite(self, state):
		if Qt.Checked == state:
			self.overwrite = True
		else:
			self.overwrite = False

	def _createStatisticsBox(self):
		statsBox = QGroupBox("Statistics")
		self.stats = Statistics()
		textWidth = self.config["display"]["statsTextWidth"]
		self.stats.create(statsBox, textWidth)

		self.mainLayout.addWidget(statsBox, 0, 7, 1, 3)

	def _createPlotsBox(self):
		plotsBox = QGroupBox("Plots")
		nbars = self.config["barPlot"]["nBars"]
		self.plots = Plots()
		self.plots.create(plotsBox, nbars=nbars)

		self.mainLayout.addWidget(plotsBox, 1, 0, 1, 10)

	def _createLogBox(self):
		logBox = QGroupBox("Log")
		self.logs = LogBox()
		self.logs.create(logBox)

		self.mainLayout.addWidget(logBox, 2, 0, 1, 10)


class Controller(object):
	"""
	Handles actions, plots, logs and statistics updates and
	input checking.
	"""
	def __init__(self, gui):
		self._gui = gui
		self._running = False
		self.timer = QTimer(self._gui)
		self.timer.timeout.connect(self._moveWaitRepeat)
		self.data = {
				"fileCount": 0,
				"runCount": 0,
				"runStarts": [],
				"runNumFiles": [],
				"fileSizes": [],
				"fileMoveTime": [],
				"fileMoveTimeTaken": [],
				"overwritten": 0
		}
		self._connectSignals()

	def _connectSignals(self):
		self._gui.startButton.clicked.connect(self._start)
		self._gui.resetButton.clicked.connect(self._resetInputs)
		self._gui.stopButton.clicked.connect(self._stop)
		self._gui.clearMenu.triggered.connect(self._clear)

	def _clear(self):
		"""
		Clear button in the Menu
		This option stops the program, clears all stored data and resets
		inputs, log box, statistics and plots.
		"""
		if self._running:
			self._stop()
			self._gui.statusBar.showMessage("Ready")

		self.data = {
				"fileCount": 0,
				"runCount": 0,
				"runStarts": [],
				"runNumFiles": [],
				"fileSizes": [],
				"fileMoveTime": [],
				"fileMoveTimeTaken": [],
				"overwritten": 0
		}
		self._gui.plots.update(self.data)
		self._gui.stats.reset()
		self._gui.logs.reset()
		self._resetInputs()

	def _start(self):
		self._gui.statusBar.showMessage("Checking inputs...")

		##
		## Input Checking
		self.regex = self._gui.regex.text()
		self.srcDir = self._gui.sourceDir.text()
		self.dstDir = self._gui.destDir.text()
		if not self._checkInputs(self.regex, self.srcDir, self.dstDir):
			return

		self._gui.logs.update("Inputs checked. OK")

		self._running = True
		self._lockInputs()
		self._moveWaitRepeat()

	def _moveWaitRepeat(self):
		self._gui.statusBar.showMessage("Getting valid files list")
		validFiles = getValidFiles(self.srcDir, self.regex)
		self._gui.logs.update(f"Found {len(validFiles)} files")

		successMoves = 0 # Number of files moved in this iteration
		fileNames = []   # Files moved in this iteration
		stop = False

		for file in validFiles:

			if not self._running:
				self.timer.stop()
				stop = True
				break

			futurePath = os.path.join(self.dstDir, os.path.basename(file))

			if not self._gui.overwrite and os.path.isfile(futurePath):
				self._gui.logs.update(f"File {os.path.basename(file)} already exists. Skipping...")
				continue

			fileSize = os.path.getsize(file) / 1000 # in kbytes
			self._gui.statusBar.showMessage(f"Moving file: {os.path.basename(file)}")
			try:
				exists = os.path.isfile(futurePath)
				moveTime = time.perf_counter()
				os.rename(file, futurePath)
				moveTime = time.perf_counter() - moveTime

				# Gathering Data
				fileNames.append(file)
				self._gui.logs.update(f"File {os.path.basename(file)} moved")
				if exists:
					self.data["overwriten"] += 1
				self.data["fileCount"] += 1
				self.data["fileSizes"].append(fileSize)
				self.data["fileMoveTimeTaken"].append(moveTime)
				self.data["fileMoveTime"].append(QDateTime.currentDateTime())
				successMoves += 1
			except Exception as E:
				print(E)

		self.data["runNumFiles"].append(successMoves)
		self.data["runCount"] += 1

		# Update plots, statistics and the log file
		self._gui.plots.update(self.data)
		self._gui.stats.update(self.data)
		self._writeLogFile(fileNames, successMoves)

		self._gui.logs.update(f"Iteration complete. {successMoves}/{len(validFiles)} files were moved.")

		now = QDateTime.currentDateTime()
		nextIt = now.addSecs(self._gui.timer.value())
		self._gui.logs.update(f"Next iteration at {nextIt.toString('yyyy-MM-dd HH:mm:ss')}")
		self._gui.logs.update("...")
		self._gui.statusBar.showMessage("Waiting...")

		if stop:
			return

		# Wait for the next iteration
		self.timer.start(1000 * self._gui.timer.value())

	def _writeLogFile(self, fileNames, nMoved):
		"""
		This function writes information to the log file for each
		file moved. Information includes: Time, file name, source dir,
		destination dir and file size

		Example:
		[YYYY-mm-dd HH:MM:SS] File filename moved from dir1 to dir2 | Size (kB): size
		"""
		if nMoved > 0:
			with open("log.txt", "a") as f:
				for i, filename in enumerate(fileNames):
					fcount = self.data["fileCount"]
					moveTime = self.data["fileMoveTime"][fcount - nMoved + i]
					fSize = self.data["fileSizes"][fcount - nMoved + i]
					fSize = str(fSize) if isinstance(fSize, int) else str(round(fSize, 2))
					timeStr = self.data["fileMoveTime"][fcount - nMoved + i].toString('yyyy-MM-dd HH:mm:ss')
					timeStr = "[" + timeStr + "]"
					text = [timeStr, "File", os.path.basename(filename), "moved from",
							self.srcDir, "to", self.dstDir, "|", "Size (kB):", fSize]
					f.write(" ".join(text) + "\n")

	def _checkInputs(self, regex, srcDir, dstDir):
		"""
		Input checking. If inputs are valid, paints the text cell with blue,
		red otherwise. Valid paths are those that exists and are writable.
		"""
		if not checkRegex(regex):
			self._gui.statusBar.showMessage("Bad Regular Expression")
			self._gui.regex.setStyleSheet("QLineEdit{background : LightPink;}")
			self._gui.logs.update("Bad Regular Expression")
			return False
		self._gui.regex.setStyleSheet("QLineEdit{background : LightBlue;}")
		
		if not validPath(srcDir):
			self._gui.statusBar.showMessage("Bad source directory")
			self._gui.sourceDir.setStyleSheet("QLineEdit{background : LightPink;}")
			self._gui.logs.update("Bad source directory. " +\
					"Directory does not exist or is not writable")
			return False
		self._gui.sourceDir.setStyleSheet("QLineEdit{background : LightBlue;}")
		
		if not validPath(dstDir):
			self._gui.statusBar.showMessage("Bad destination directory")
			self._gui.destDir.setStyleSheet("QLineEdit{background : LightPink;}")
			self._gui.logs.update("Bad destination directory. " +\
					"Directory does not exist or is not writable")
			return False
		self._gui.destDir.setStyleSheet("QLineEdit{background : LightBlue;}")
		self._gui.timer.setStyleSheet("QSpinBox{background : LightBlue;}")
		
		return True

	def _resetInputs(self):
		"""
		Clear text inputs and reset timer to default
		"""
		self._gui.regex.setText("")
		self._gui.sourceDir.setText("")
		self._gui.destDir.setText("")
		self._gui.timer.setValue(self._gui.config["spin"]["defaultValue"])

	def _lockInputs(self):
		"""
		Disables input editing while the program is running
		"""
		self._gui.regex.setReadOnly(True)
		self._gui.sourceDir.setReadOnly(True)
		self._gui.destDir.setReadOnly(True)
		self._gui.startButton.setEnabled(False)
		self._gui.resetButton.setEnabled(False)
		self._gui.timer.setReadOnly(True)

	def _unlockInputs(self):
		"""
		Unlocks text inputsand timer and removes text cells background color
		"""
		self._gui.regex.setReadOnly(False)
		self._gui.sourceDir.setReadOnly(False)
		self._gui.destDir.setReadOnly(False)
		self._gui.startButton.setEnabled(True)
		self._gui.resetButton.setEnabled(True)
		self._gui.timer.setReadOnly(False)

		self._gui.timer.setStyleSheet("")
		self._gui.regex.setStyleSheet("")
		self._gui.sourceDir.setStyleSheet("")
		self._gui.destDir.setStyleSheet("")

	def _stop(self):
		self._running = False
		self._unlockInputs()
		self.timer.stop()
		self._gui.statusBar.showMessage("Stopped")


def main():
	with open("config.json", "r") as f:
		config = json.load(f)

	app = QApplication([])
	gui = MoveFileAppUI(config)
	gui.show()

	ctrl = Controller(gui)

	sys.exit(app.exec_())


if __name__ == "__main__":
	main()