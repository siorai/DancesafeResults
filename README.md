# DancesafeResults

Web application to be hosted locally while Dancesafe Chapters are on site in order to better record reagent results.

## About
This project is for the better collection of reagent testing results and a whole lot more for Dancesafe chapters across the world. 

As of right now I'm envisioning this having 2 large portions of it, firstly is this part, a localized version that will eventually live on a raspberry pi 3. 

The end result should be an image that'll be easily burnable to a 16GB MicroSD card and plugged directly into a raspberry pi and be good to go. Granted, I'm a long away from that.... 

## Requirements

Right now the python requirements should be listed in the setup.py, but outside of that you'll need access to a postgresql server running wherever. Currently I have mine running locally. 

## TODO
- [x] populate TODO list with actual TODO items
- [x] hammer out missing details/complete database schema
- [ ] .... then change large portions of it and finish refactoring those
- [ ] WRITE DOCUMENTATION OUT
- [ ] Start working on an overall installation guide for people that don't want to use the image files that I'll generate
- [ ] Redesign html pages to Bootstrap Material
- [x] Swap all instances of IDs with UUIDs to prevent duplicate primary keys when remote db's merge into a centralized db
- [ ] Outline just what that centralized db will even look like and where it'll even live
- [ ] Finish compiling PostgreSQL 10.0 on QEMU's Raspberry Pi 3 emulater since if it compiles successfully while emulating the Raspberry Pi 3's ARM8 CPU, there's no reason to think that PostgreSQL 10 won't compile on a real one
- [x] Refactor UUID call to work properly. ( as of 10:27 PM Pacific 10/16/2017 it's as broken as the Epic Level Handbook ) The first post for /add_question successfully adds a row to the table, but the second time, it returns with a duplicate primary key(the UUID) which leads me to believe that the function that I have in place for generating that UUID only executes once when I initially run the flask run. Restarting gives me a new UUID. 
- [ ] Redesign main survey page to include a navigation bar that'll let users goto the other forms for adding things like additional users, events, questions, etc etc
- [ ] Figure out exactly what 'etc etc' means, ie what other database entries the users will be able to insert outside of the normal survey POST
- [ ] Outline an administrator page for the pi for chapter presidents and officers to access and what should be in it
- [x] Hash out most recent ideas for the tracking/recording of individual color reactions as per conversation with Dave-
        - Currently there's been a bit of a debate between what datatype to store the colors in the database as. Of the people I've spoken to, each person seems to be split down the middle between using strings ( just literally typing in the name of the color and storing it as a string) or a 32 bit integer in the form of more standard RGB Hex code.  Over the past couple of days I've made both just to see how it works. Ultimately I think I'll be going with the hexcode since it doesn't leave as much room for interpretation. In that same /add_question form that kind of just turned into the add_data form, there's a set of three color.picker() javascript objects where the user can click one and then select a color in a similar fashion as MS Paint from the 1800s. So the advantage to doing it this way, is it makes it much easier to compare the colors since I can just write queries and views that compare those values, which isn't something I can do with color strings of course. 
- [ ] Also need to hash out the other idea I've had kicking around for a while, which is somehow autopopulating and/or otherwise display to the screen the expect colors based on what they expect the substance to be. This would come in the form of a drop down, where the first color in the list would be what's expected, however, the next 2-4 rows would be populated and picked based on a queury that checks the previous color reactions on that particular substance.  Theoretically this should greatly decrease the amount of time it takes for colors to be selected which, historically, has been the biggest bottleneck when it comes to recording reagent results in either digital or analogue form. 
- [ ] Ask various people that have done released studies and compiled data based on reagent results to see what kind of information they would like to inquire about in order to get better ideas on createing more Views. 
