[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# DancesafeResults

Web application to be hosted locally while Dancesafe Chapters are on site in order to better record reagent results.

## About
This project is for the better collection of reagent testing results and a whole lot more for Dancesafe chapters across the world. 

As of right now I'm envisioning this having 2 large portions of it, firstly is this part, a localized version that will eventually live on a raspberry pi 3. 

The end result should be an image that'll be easily burnable to a 32GB MicroSD card and plugged directly into a raspberry pi and be good to go. Granted, I'm a long away from that.... 

## Requirements

Right now the python requirements should be listed in the setup.py, but outside of that you'll need access to a postgresql server running wherever. Currently I have mine running locally. Front requirements are should listed in the package.json inside of the frontend subdir.  

## TODO
- [ ] Finish up authorization complete with login/logout and isolate password storage in database
- [ ] Normalize data from ecstasydata from JSON into easier to handle datatypes and tables in database

## Special Thanks

* [Kliment](https://github.com/kliment)- For originally suggesting I put this all on a raspberry pi 3 to begin and all the sage advice on db design. 
* [Multiplexd](https://github.com/multiplexd) - For helping me figure out a partitioning issue that had stumped me for weeks.  
