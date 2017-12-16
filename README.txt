University of Central Florida
Evolutionary Computation Lab
Author: Aidan Lakshman

I ran this program using Python 3.5

Required python3 packages: pandas, matplotlib, numpy, scipy, python3-pip, ggplot

Run "python3 mainGA.py" to start the algorithm.  
Algorithm will prompt you for how many generations you want to iterate through.
Users have the option of saving checkpoints as pickle files, then loading them in when calling "python3 mainGA.py"

It's important to note that you must have the correct installation of ggplot.
"pip3 install ggplot" did not work correctly for me on my machine (Ubuntu 16.04 LTS, Python 3.5)
If you pip install ggplot and receive an error message related to a sort function not working, 
try running the ggplotFix.sh shell script. 
Note that I don't have much experience with shell scripts, so there's a good chance it won't work.

If the script doesn't work or you don't want to run it, do the following:

1. Open terminal and input the following commands (replace pip with pip3 if necessary):

pip uninstall ggplot
pip install git+git://github.com/yhat/ggpy.git@9d00182343eccca6486beabd256e8c89fb0c59e8 --no-cache

2. After you have downloaded this version of ggplot, locate the ggplot.py script
	-Mine is located at usr/local/lib/python3.5/dist-packages/ggplot/ggplot.py
	-If you're really having trouble, you can open a python interactive shell and type the following:
		import site
		site.getsitepackages()
	-You should get a list containing the path to the dist-packages
	-ggplot.py is located inside of the dist-packages/ggplot folder

3. open the ggplot.py script in any text editor and replace line 602 with the following:
	fill_levels = self.data[[fillcol_raw, fillcol]].sort_values(by=fillcol_raw)[fillcol].unique()

4. save and you should be good to go!
