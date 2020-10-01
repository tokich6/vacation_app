from os import environ
from flask import Flask, render_template, request, redirect, session, flash
# , flash, jsonify, session
# from flask.ext.session import Session
# from tempfile import mkdtemp
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash

from helpers import search_location_id, list_properties

# Configure application
app = Flask(__name__)

# Set the sessions' secret key to some random bytes. 
app.secret_key = environ.get('SECRET_KEY')


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/hotels", methods=['GET', 'POST'])
def search_api():
    if request.method == 'GET':
        return render_template('hotels.html')
    else:
        # extract parameters from the search form
        destination = request.form.get('destination')
        print(destination)
        check_in = request.form.get('check-in')
        print(check_in)
        check_out = request.form.get('check-out')
        print(check_out)
        rooms = request.form.get('rooms')
        print(rooms)
        adults_room1 = request.form.get('adult1')
        print(adults_room1)


        # search_location_id defined in helpers.py
        destinationID = search_location_id(destination)
        # print(f'destinationID is: {destinationID}')
        
        if not destination:
            flash('Please type in a location')
            return redirect("/")
        else:
            # list_properties defined in helpers.py
            output = list_properties(destinationID, check_in, check_out, adults_room1)
            header = output['header']
            totalCount = output['totalCount']
            # an array of hotels' list
            hotels = output['hotels']
            print(hotels[0])
            return render_template('hotels.html', header=header, totalCount=totalCount, hotels=hotels)


@app.route("/hotels/<hotelID>", methods=['POST'])
def show_hotel_details(hotelID):
    hotel_id = request.form.get('hotel_id')
    print(f'Hotel_id is: {hotel_id}')
    return render_template('hotel_details.html', hotelID=hotel_id)
    

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Forget any user_id
    # session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username", 403)
            return redirect ('/login')

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password", 403)
            return redirect ('/login')

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        username = rows[0]['username']

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password", 403)
            return redirect ('/login')

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash('You were successfully logged in')
        # Redirect user to home page
        return redirect("/account")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')    

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.debug = True
    app.run()