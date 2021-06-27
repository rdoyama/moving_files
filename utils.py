"""
Some useful and general method and classes
"""

from PyQt5.QtWidgets import QLabel, QVBoxLayout

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
	def show(self, Widget, data):
		text = """
			<br>Average: {} saushuhauhusdgyagsdasdgahg</br>
			<br>Other statistics</br>
		""".format(sum(data)/len(data))

		boxLayout = QVBoxLayout()

		textLabel = QLabel(text)
		boxLayout.addWidget(textLabel)
		Widget.setLayout(boxLayout)

	