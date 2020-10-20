from os import environ
from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# jsonify, session
# from flask.ext.session import Session
# from tempfile import mkdtemp
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


from helpers import search_location_id, list_properties, get_hotel_details, get_hotel_photos, login_required

# Configure application
app = Flask(__name__)

# Set the sessions' secret key to some random bytes. 
app.secret_key = environ.get('SECRET_KEY')

# define global variables
check_in = ''
check_out = ''
adults_room1 = ''
rooms = ''

# DATABASE SETUP AND SCHEMAS START
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

# schemas
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

# DATABASE SETUP AND SCHEMAS END


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/hotels", methods=['GET', 'POST'])
def list_hotels():
    if request.method == 'GET':
        return render_template('hotels.html')
    else:
        # extract parameters from the search form
        destination = request.form.get('destination')
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
        
        if not destination:
            flash('Please type in a location')
            return redirect("/")
        else:
            # list_properties defined in helpers.py
            output = list_properties(destination_id, check_in, check_out, adults_room1)
            header = output['header']
            totalCount = output['totalCount']
            # an array of hotels' list
            hotels = output['hotels']
            # print(hotels[0])
            return render_template('hotels.html', header=header, totalCount=totalCount, hotels=hotels)

@app.route("/hotels/details", methods=['GET', 'POST'])
def show_hotel_details():
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
    return render_template('confirm_booking.html')

@app.route("/account", methods=['GET', 'POST'])
@login_required
def your_bookings():
    return render_template('your_bookings.html')

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            flash("Please provide a username", 403)
            return redirect ('/register')
        # Query database for username
        elif db.session.query(Profile).filter(Profile.username == username).count() != 0:
            flash("The username already exists, please log in if previously registered or choose a different one", 403)
            return redirect ('/register')

        email = request.form.get("email")
        if not email:
            flash('please provide an email address', 403)
            return redirect('/register')
        elif db.session.query(Profile).filter(Profile.email == email).count() != 0:
            flash("The email address you entered is already associated with an account, please log in", 403)
            return redirect ('/login')    

        password = request.form.get("password")
        # Ensure password was submitted
        if not password:
            flash("must provide password", 403)
            return redirect ('/register')

        confirm_password = request.form.get("confirm-password")
        # enfure confirmation was submitted and matches the password
        if not confirm_password:
            flash("must confirm password", 403)
            return redirect ('/register')
        elif confirm_password != password:
            flash("confirm password is not a match", 403)
            return redirect ('/register')

        # hash the password
        hash = generate_password_hash(password)

        # enter data into database 
        data = Profile(username, email, hash)
        db.session.add(data)
        db.session.commit()
        # success
        flash('You have registered successfully!')
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Forget any user_id
    session.clear()
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

        rows = db.session.query(Profile).filter(Profile.username == request.form.get('username')).all()
        
        match = check_password_hash(rows[0].hash, request.form.get("password"))
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not match:
            flash("invalid username and/or password, please try again", 403)
            return redirect ('/login')

        # Remember which user has logged in
        session["user_id"] = rows[0].id
        session['username'] = request.form['username']

        flash('You are successfully logged in!')
        # Redirect user to home page
        return redirect('/index')
        # return redirect(request.referrer)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')    

@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.run()