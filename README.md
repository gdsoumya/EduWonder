# EduWonder
EduWonder is a collaborative learning platform that allows teachers and students to share and explore references and educational materials. 

EduWonder allows it's users to create communities/groups to share information, ask questions, upload and share documents and files. This is a basic open-source structure that allows anyone to add in new features according to their needs.

This project was created as an entry for the **Mozilla Hello Web Hackathon 3.0 @Mozilla Bhubaneswar** and had made it to the final round.
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

**EduWonder** requires [ **Python (Python 2.7)**](https://www.python.org/) .

### Getting the project.
```sh
$ git clone https://github.com/gdsoumya/EduWonder.git
or 
Download and extract the Zip-File
```

### Setting up Virtual Environemt
Setting up a virtual environment would be better for both development and normal execution purposes.
```sh
$ cd EduWonder
$ python -m virtualenv env
$ source env/bin/activate
 or (Windows machine)
$ .\env\Scripts\activate
```
### Installing Dependencies
The Project has a few dependencies which can be installed by running.
```sh
$ pip install -r dependencies.txt 
```
## Setting up the Database
This project uses a **mysql** database, the database can be changed in the '[.flaskenv](https://github.com/gdsoumya/EduWonder/blob/master/.flaskenv)' file under the '**DATABASE_URL**'.

To initialize the database run
```sh
$ flask db init
```
To run the database migrations use
```sh
$ flask db migrate
$ flask db upgrade
```
## Starting Server
To start the Flask server run
```sh
$ flask run
```
A Flask development server will be initialized at http://127.0.0.1:5000/

## Packages Used
- **[Flask](https://flask.pocoo.org/)** : For the backend server.
- **[Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)** : For integrating the database.
- **[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)** : For database migrations.
- **[Flask-Login](https://flask-login.readthedocs.io/en/latest/)** : For handling user login.
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** : For setting up environment variables.

## Author
-   **Soumya Ghosh Dastidar** (Backend)
-   **Suchismita Banerjee** (Front-end)
-   **Disha Kar** (Front-end)

## Contributting
Any contribution/suggestions are welcomed.
