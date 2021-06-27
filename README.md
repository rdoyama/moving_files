# Moving Files Application

This is a small Python3 application that moves files whose names match a user input regular expression. The source and destination directories are specified by the user and can not be remote directories. As long as the program is running, the code checks if there are new valid files in the source directory based on a timer and continuously shows plots and statistics regarding the files that were moved.

This program was written and tested in a Linux machine with Python 3.8.

## Dependencies

 - [PyQt5](https://pypi.org/project/PyQt5/)
 - [Matplotlib](https://matplotlib.org/stable/users/installing.html)

## Installation & Usage

After the installation of the dependencies, download (or clone) this repository and extract all files. To run the program, switch to the extracted folder and execute the main script.

```bash
$ cd moving_files
$ python3 app.py
```

Finally, write down the regular expression, source and output directories and set the timer. Click "Start" when ready and the program will start moving the files (if there is any). The progress can be tracked with the statistics and plots boxes or the status bar.
