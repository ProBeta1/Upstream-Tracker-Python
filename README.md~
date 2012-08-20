Upstream-Tracker-Rails
======================

Setting up the stage

The project is split into two parts – the web frontend based on Rails and the backend based on Python. In this document, we will look only at the Python backend – how it works, how to set it up, how to use it and it's API calls. In this section, I shall explain in brief, how to set things up using Ubuntu OS as an example. 

Setting up the python environment

The python environment is very easy to set up as it is installed by default on almost all the major linux distributions. Currently, the code runs on python 2.7. However, it requires the BeautifulSoup module to work. This can be found and installed using the distro's package manager. 

Running the Python backend

To start processing the records using the python backend, clone the git repository found at https://github.com/nbprashanth/Upstream-Tracker-Python.git. Once cloned, change into the directory and run the main.py using the command python main.py.

Changing essential parameters

Many parameters used in the code can be varied. These would ideally be given as input using the command line arguments, however, currently, these are defined inside main.py. Hence, it is necessary to modify these parameters before running the code. Some of the parameters that should/can be modified are :

THREAD_LIMIT : Sets the maximum number of threads that run simultaneously.
QUEUE_LIMIT : Sets the maximum number of jobs/tasks that are in the queue waiting to be processed at any given point of time. 
URL : This is the URL of the Rails web frontend. If it is running locally, this is usually http://localhost.
PORT : Port on which the Rails server is listening. This is by default 3000.

What's missing?

The Upstream Tracker was developed as a part of Google Summer of Code 2012 during a three month interval. Hence, there is a lot of scope for the project to be improved. Some of the current features that are lacking which can be worked upon for the future versions are :

	1. Implement backend for comparison of packages of a particular system with upstream versions.
