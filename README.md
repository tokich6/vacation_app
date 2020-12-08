# Home Away - hotel booking web app

Web-based hotel app - using Python, Javascript and SQL

Using [rapidapi](https://rapidapi.com/apidojo/api/hotels4)for hotel data (based on hotels.com API). Register for free and create get your API key if planning on running this project locally.

## Motivation for this project

My background in Travel and in particular, online travel agencies is what motivated me for this project.

## Project Description 

The web app lets you check for hotel availability based on location, dates, number of rooms, guests. The data can also be sorted by price, star rating, reviews, etc. 

The app consists of 11 routes alltogether,  3 of which (/register, /login, /logout) are partly based on the web track's distribution code.

The information needed for the hotels search is gathered on the /index route and the results (available hotels) are then dispalyed on the /hotels route. Each hotel 'card' contains information such as reviews, star rating and prices as well as a link to more information about that specific hotel.
That is the  /hotels/details route which displays hotel images from the API as a carousel (carousel functionality implemented in JavaScript), additional location details and a link to make a booking. 

The /booking route is where a final call to the API is made to check room availability before confirmation - the available room name, image, price and booking conditions are dispayed here (the app restricts the availability to the first room offered by the hotel due to limited API calls available for the account used). The user is asked to confirm all details and enter a guest name in order to complete the booking. The details are then sent to a PostgreSQL database. The database contains 2 tables - users and bookings. Flask-SQLAlchemy extension for Flask is utilized in the application. For local development, I've used [Postgres.app](https://postgresapp.com/) and [pgAdmin4](https://www.pgadmin.org/) as a graphical client.

Upon successful reservation, the /account route is displayed listing all bookings made, incl the newly confirmed one. The route also offers the functionality to filter bookings by confirmed or cancelled category. Each booking also offers cancel booking functionality (if refundable) which uses a POST method to send the booking id to the /cancellation route where the booking status is changed from confirmed to cancelled in the database.
Each confirmed booking also has a download booking voucher functionality as a pdf, utilizing [pdfkit](https://pypi.org/project/pdfkit/). 

The app utilizes [TailwindCSS CDN](https://tailwindcss.com/) - a utility-first CSS framework to achieve its custom designs.

The helpers.py file consists of helper functions, e.g. making API calls and others.

## Installation and running

1. git clone or fork the project source code. Requires Python version of 3.8.

2. install pipenv - creates and manages a virtual environment for your projects as well as adds/removes packages from Pipfile as you install/uninstall packages

```
pip install pipenv
```

3. cd into the projects directory and install required packages. To initialize a Python 3 virtual environment, run $ pipenv --three.


```
pipenv install
```

4. Create a .env file in the main directory and add SECRET_KEY and API_KEY to it (instructions provided at the beginning of this file on where to register to get an API key).

5. To spawn a shell with the virtualenv activated (make sure you're in the projects directory)

```
pipenv shell
```

6. Finally, to run the application 

```
python app.py
```

7. Open app on localhost http://127.0.0.1:5000/
