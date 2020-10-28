from os import environ
from datetime import date, timedelta
from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# jsonify, session
# from flask.ext.session import Session
# from tempfile import mkdtemp
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


from helpers import search_location_id, list_properties, get_hotel_details, get_hotel_photos, login_required, get_days

# Configure application
app = Flask(__name__)

# Set the sessions' secret key to some random bytes. 
app.secret_key = environ.get('SECRET_KEY')

# define global variables
check_in = ''
check_out = ''
adults_room1 = ''
rooms = ''

# DATABASE SETUP START
ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    # connect to development database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/homeaway'
else:
    app.debug = False
    # connect to production database
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize db
db = SQLAlchemy(app)

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique = True, nullable = False)
    hash = db.Column(db.Text, nullable=False)

    def __init__(self, username, email, hash):
        self.username = username
        self.email = email
        self.hash = hash

# DATABASE SETUP END

# ROUTES START HERE
@app.route("/", methods=['GET', 'POST'])
def index():
    tomorrow = date.today() + timedelta(days=1)
    day_after = date.today() + timedelta(days=2)
    return render_template('index.html', tomorrow=tomorrow, day_after=day_after)

@app.route("/hotels", methods=['GET', 'POST'])
def list_hotels():
    if request.method == 'GET':
            return redirect("/")
    else:
        # extract parameters from the search form
        destination = request.form.get('destination')
        print(destination)
        global check_in
        check_in = request.form.get('check-in')
        print(check_in)
        global check_out
        check_out = request.form.get('check-out')
        print(check_out)
        global rooms
        rooms = request.form.get('rooms')
        print(rooms)
        global adults_room1
        adults_room1 = request.form.get('adult1')
        print(adults_room1)

        # search_location_id defined in helpers.py
        destination_id = search_location_id(destination)
        print(f'destination id is { destination_id  }')
        

        if not destination:
            flash('Please type in a destination', 'error')
            return redirect("/")
        elif not check_in or not check_out:
            flash('Please provide a valid check-in and check-out date', 'error')
            return redirect("/")
        else:
            # list_properties defined in helpers.py
            output = list_properties(destination_id, check_in, check_out, adults_room1)
            print(output)
            if output == None:
                return render_template('400.html')
            header = output['header']
            totalCount = output['totalCount']
            # an array of hotels' list
            hotels = output['hotels']
            # print(hotels[0])
            return render_template('hotels.html', header=header, totalCount=totalCount, hotels=hotels)

@app.route("/hotels/details", methods=['GET', 'POST'])
def show_hotel_details():
    # add POST method
    # hidden input value in hotels.html
    hotel_id = request.form.get('hotel_id')
    print(f'Hotel_id is: {hotel_id}')
    print(check_in)
    print(check_out)
    print(adults_room1)
    
    # get_hotel_details function defined in helpers
    output_hotel_details = get_hotel_details(hotel_id,check_in, check_out, adults_room1)
    # save necessary output results as variables to access in template
    amenities = output_hotel_details['amenities']
    what_is_around = output_hotel_details['what_is_around']
    hotel_name = output_hotel_details['property_description']['name']
    hotel_stars = output_hotel_details['property_description']['starRating']
    hotel_address = output_hotel_details['property_description']['address']['fullAddress']
    tagline = output_hotel_details['property_description']['tagline']
    freebies = output_hotel_details['property_description']['freebies']
    hotel_price = output_hotel_details['property_description']['featuredPrice']['currentPrice']['formatted']
    hotel_rooms = output_hotel_details['property_description']['roomTypeNames']

    # get_hotel_photos defined in helpers 
    output_hotel_photos = get_hotel_photos(hotel_id)
    hotel_images_list = output_hotel_photos['hotel_images']
    # loop through images, format size & add image urls to list
    images_url_list = []
    for image in hotel_images_list:
        size = image['sizes'][0]['suffix']
        image_url = image['baseUrl'].format(size=size)
        images_url_list.append(image_url)
    

    return render_template('hotel_details.html', hotelID=hotel_id, hotel_name=hotel_name, hotel_stars=hotel_stars, hotel_address=hotel_address,
     hotel_price=hotel_price,amenities=amenities, what_is_around=what_is_around, tagline=tagline, freebies=freebies, hotel_rooms=hotel_rooms, images_url_list=images_url_list)
    
@app.route("/booking", methods=['GET', 'POST'])
@login_required
def confirm_booking():
    if request.method == 'POST':
        
        hotel_id = request.form.get('hotel_id')
        hotel_price = request.form.get('hotel_price')

        # contact API to check details as well as room rates before final booking confirmation
        output_hotel_details = get_hotel_details(hotel_id, check_in, check_out, adults_room1)

        hotel_name = output_hotel_details['property_description']['name']
        hotel_stars = output_hotel_details['property_description']['starRating']
        hotel_address = output_hotel_details['property_description']['address']['fullAddress']
        best_room = output_hotel_details['rooms'][0] # returns an array
          # get_days defined in helpers.py
        stay_duration = get_days(check_in, check_out)
    
        return render_template('confirm_booking.html', check_in=check_in, check_out=check_out, hotel_rooms=rooms, adults_room1=adults_room1,
        hotel_id=hotel_id, hotel_name=hotel_name, hotel_stars=hotel_stars, hotel_address=hotel_address, hotel_price=hotel_price, room=best_room,
        stay_duration=stay_duration)

    # else request is GET
    return redirect('/')

@app.route("/account", methods=['GET', 'POST'])
@login_required
def your_bookings():
    return render_template('your_bookings.html', name=session['username'])

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            flash('Please provide a username', 'error')
            return redirect ('/register')
        # Query database for username
        elif db.session.query(Profile).filter(Profile.username == username).count() != 0:
            flash('The username already exists, please log in if previously registered or choose a different one', 'error')
            return redirect ('/register')

        email = request.form.get("email")
        if not email:
            flash('please provide an email address', 'error')
            return redirect('/register')
        elif db.session.query(Profile).filter(Profile.email == email).count() != 0:
            flash('The email address you entered is already associated with an account, please log in', 'error')
            return redirect ('/login')    

        password = request.form.get("password")
        # Ensure password was submitted
        if not password:
            flash('must provide password', 'error')
            return redirect ('/register')

        confirm_password = request.form.get("confirm-password")
        # enfure confirmation was submitted and matches the password
        if not confirm_password:
            flash('must confirm password', 'error')
            return redirect ('/register')
        elif confirm_password != password:
            flash('confirm password is not a match', 'error')
            return redirect ('/register')

        # hash the password
        hash = generate_password_hash(password)

        # enter data into database 
        data = Profile(username, email, hash)
        db.session.add(data)
        db.session.commit()
        # success
        flash('You have registered successfully!', 'success')
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Forget any session user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # get the value of the hidden next url input
        next_url = request.form.get("next")
        # Ensure username was submitted
        if not request.form.get("username"):
            flash('must provide username', 'error')
            return render_template ('login.html')

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('must provide password', 'error')
            return render_template ('login.html')

        # query database for the username input
        user = db.session.query(Profile).filter(Profile.username == request.form.get('username')).first()

        # Ensure username exists and password is correct
        if not user or not check_password_hash(user.hash, request.form.get("password")):
            flash('invalid username and/or password, please try again', 'error')
            return render_template ('login.html')

        # Remember which user has logged in
        session["user_id"] = user.id
        session['username'] = request.form['username']

        # check if we're redirecting the user to another endpoint, if not default
        if next_url:
            return redirect(next_url)
        flash('You are successfully logged in!', 'success')
        return redirect(url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')    

@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    return redirect("/")

# custom templates for error handling - to be added

# @app.errorhandler(404)
# def not_found():
#     """Page not found."""
#     return make_response(render_template("404.html"), 404)


# @app.errorhandler(400)
# def bad_request():
#     """Bad request."""
#     return make_response(render_template("400.html"), 400)


# @app.errorhandler(500)
# def server_error():
#     """Internal server error."""
#     return make_response(render_template("500.html"), 500)


if __name__ == '__main__':
    app.run()