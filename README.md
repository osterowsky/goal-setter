# **GOALSETTER**
## **Video Demo:**  https://youtu.be/-gWG3L4m7bw
## **Description:**

The project is called GoalSetter and is MVP of MVPs. It took a few days to complete and is very simple
in functionality.

The backend of the project was developed using Python and Flask as a micro-framework.
For frontend obviously HTML, CSS and JavaScript were used.
The database used in the project was Sqlite3

## **Let's start by describing utility**

Basically, after succesfully registering and loggingg, user has access to panel
for setting his own tasks, he can delete some of them or mark them while finished.
Achieved tasks users can find in subpage called "Finished".
Of couse everything is stored in a session to save time for active users, if they want to
there is a very simple option to log out from web service.

## **Let's talk backend**

Python and Flask was chosen by its simplicity to simple POST, GET requests.
The app contains multiple routes and makes UX very intuitively.
It handles login, register or logout routes for smooth experience in connecting to web service.
Also it handles our main page for setting, deleting or marking finished tasks

## **Let's talk about database**

Sqlite3 was choosen based on its simplicity and lightweight, which is perfect for minimum version of
product like this. Everyhing works very smoothly with that technology.
Database store two tables. First one stores information about users, their username, id
and hashed password to confirm security.
Second table is about tasks, which associate the tasks based on their type "PLAIN" and "FINISHED"
to distinguish in which page show which tasks.
Also it connects tasks to userID using foreign key.

## **Let's finish at frontend**

There are 5 pages structed, layout which stores universal structure for all other pages.
Main page, which shows different information if user is authenticated or not (Logged in users see panel to set their tasks and unlogged can only see marketing taglines).
Login and register pages only contains headling and essential input fields for their prime purposes.
The "finished" page is only available for logged users and shows achieved already tasks.
The whole design is stored in a style.css file, 2 fonts were mainly used and 4 colors (white, black, dark blue & royal blue).
Everything was designed with the help of framework called Bootstrap. JavaScript is used only once to show the toggle menu for mobile or tablet users.
The favicon of web service was borrowed from the site SVG Repo.
