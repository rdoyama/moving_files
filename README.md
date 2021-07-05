# Moving Files Application

This is a small Python3 application that moves files whose names match a user input regular expression. The source and destination directories are specified by the user and can not be remote directories. As long as the program is running, the code checks if there are new valid files in the source directory based on a timer and continuously shows plots and statistics regarding the files that were moved.

This program was written and tested in a Linux machine with Python 3.8.

<img src="https://i.ibb.co/JjsntRC/Screenshot-from-2021-06-30-14-20-46.png" alt="Your image title" width="700"/>

## Dependencies

 - [PyQt5](https://pypi.org/project/PyQt5/)
 - [Matplotlib](https://matplotlib.org/stable/users/installing.html)

## Installation & Usage

After the installation of the dependencies, download (or clone) this repository and extract all files. To run the program, switch to the extracted folder and execute the main script.

```bash
$ cd moving_files
$ python3 app.py
```

Finally, write down the regular expression, source and output directories and set the timer. Click "Start" when ready and the program will start moving the files (if there are any). The progress can be tracked with the statistics and plots boxes or the status bar.

**Caution**: Closing/quitting the program while it is running may corrupt files.

## Menu & Buttons
The menu is simple and allows the user to change the window style, clear all data generated during the last run of the program, exit and show program information.

In the main window there ate three buttons: "Start", "Stop" and "Reset". The "Start" button checks if the inputs are valid: the regular expression must compile and the source/destination directories exist and are writable. The "Stop" button stops the iteration and the "Reset" button clears all inputs and sets the timer to the default value.

## Configuration File

 - `initialWidth` and `initialHeight`define the width and height of the main window. The minimum recommended values are 1000 and 7000, respectively.
 - `statsTextWidth` is the size of each line in the statistics box measured in characters. The minimum recommended value is 30.
 - `defaultValue`, `minValue` and `maxValue` are used to limit the lower and upper bounds and the default value for the timer, measured in seconds.
 - `nBars` controls the number of iterations that will be plotted in the bar plot (the number of files moved in each iteration for the last `nBars` iterations).

## Log File
When the program starts, it will create a log file named `log.txt` in the same directory of the main program, if it does not exist already. This file will be updated at the end of each iteration, and each line contains the time when the file was moved, the name of the file, the source and destination directory, and the file size in kB.
