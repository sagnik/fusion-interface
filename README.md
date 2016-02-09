## Interface for Fusion: IST441 Sp. 2016

This is a python (Django) based interface for displaying search results from Lucidworks, developed for the course IST 441 @IST Pennstate (http://clgiles.ist.psu.edu/IST441/).  

###Dependencies

There are couple of dependencies to be resolved using pip (an installation tool for python) 

Django=1.5.1 (pip install Django=1.5.1) [https://www.djangoproject.com/]

requests (pip install requests) [http://docs.python-requests.org/en/latest/]

### Settings
Change the following parameters in `fusion-interface/settings.py`

BASEURL= base url of your lucidworks installation, such as **'http://ist441.ist.psu.edu:8764'** 

COLLECTION= name of your collection in Lucidworks, such as **'giles-crawl1'** 

USERNAME=#your user name for Lucidworks, usually **'admin'** 

PASSWORD=#your password for Lucidworks, such as **'TeamAdmin123'** 

###To run the code 
go to the directory fusion-interface and run 

`python manage.py runserver <hostname:port>`, for example, 

`python manage.py runserver ist441.ist.psu.edu:8000`. Use `nohup` or `screen` for running the code on a server.

###Notes

This code is not to be used in production, always keep `DEBUG=True` in settings. 

