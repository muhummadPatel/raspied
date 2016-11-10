# RASPIED Web App: Managing Remote Shared Access to an Educational Robot
The RASPIED web app was developed as part of a Computer Science Honours project at the University of Cape Town. The project had the aim of designing and implementing a complete educational robot platform built using easily accessible hardware and software. It was developed with the intention of being used in the CSC1010H Python-based introductory Computer Science course at UCT. The robot platform consists of a Raspberry Pi based robot, and a controlling web app. The distinguishing feature of the RASPIED project is it's use of a single robot to be shared among the entire class. This repository contains the code for the web app component of the project.

The robot (shown in the image below) is able to move and supports various 'extra' features (viz. a camera with colour detection capabilities, an ultrasonic distance sensor, infra-red obstacle detection, and three coloured LEDs). The robot is programmable in Python and exposes a simple API for use by students.

The subject of this paper is the design, implementation, and evaluation of the controlling web app. The web app facilitates student interactions with the robot by providing a live video stream of the robot and allowing students to write and upload code to the robot. Access to the robot is managed by requiring students to book time slots during which they are allowed to upload and run code on the robot. This booking functionality facilitates the shared access to the robot and ensures that only a single student has control over the robot at any given time.

## Getting Started
These instructions will walk through the process of setting up the RASPIED web app. If you have any problems or questions, please feel free to open an issue, or send me an email at muhummad.patel@gmail.com.

### Prerequisites
You will need the following to set up a copy of the web app:

* Python 2.7
* Virtualenv
* git
* node + npm
* redis
* sqlite

### Running the Web App
First acquire a copy of the web app by cloning or downloading this repository. Ensure that all prerequisites (as outlined in the section above) are installed and functioning. You will now need to add a new python file called secrets.py to the raspied app folder. The secrets.py folder contains setup information that should **not** be committed to the repository. You will need to populate the secrets.py file before running the raspied web app. The specific variables you need to define in the secrets.py file are outlined below:

* `DJANGO_SECRET_KEY` - the csrf token for your django web app. You can generate one [here](http://www.miniwebtool.com/django-secret-key-generator/).
* `STREAMING_SERVER_IP` - the address of the video streaming server
* `ROBOT_HOSTNAME` - the address of the raspied robot
* `ROBOT_USERNAME` - a valid username to use for SSH sessions to the raspied robot
* `ROBOT_PWD` - password for `ROBOT_USERNAME`


In order to install dependencies, navigate to the project folder and do the following:

* Set up a python virtualenv for this project  and activate it *[optional but recommended]*
* Run `pip install -r requirements.txt` to install python dependencies
* Run `npm install` to install javascript dependencies
* Run `python manage.py migrate` to set up the database


You will now be able to run a dev instance of the web app as follows:

* Run `redis-server` to start a redis instance (for Django Channels backend). Do this in a separate terminal or as a quiet background process
* Activate the virtualenv you set up for this project
* Run `python manage.py runserver`
* Go to `localhost:8000` in your web browser to access a dev version of the web app

## Deployment
Make sure that `DEBUG` is set to `False` in raspied/settings.py

## Built With
* Python [Django](https://www.djangoproject.com/) - Web framework
* JavaScript with [jQuery](https://jquery.com/) - Client-side scripting
* [Materialize](http://materializecss.com/) - Frontend CSS framework
* [pip](https://pip.pypa.io/en/stable/) - Python dependency Management
* [npm](https://www.npmjs.com/) and [bower](https://bower.io/)- Javascript dependency management

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## RASPIED Project Website
For more information about the RASPIED project, see the [RASPIED project website](https://people.cs.uct.ac.za/~ptlmuh006/)
