from os import environ
from flask import Flask, render_template, request, redirect, session, flash
# , flash, jsonify, session
# from flask.ext.session import Session
# from tempfile import mkdtemp
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash

from helpers import search_location_id, list_properties, get_hotel_details, get_hotel_photos

# Configure application
app = Flask(__name__)

# Set the sessions' secret key to some random bytes. 
app.secret_key = environ.get('SECRET_KEY')

# define global variables
check_in = 'null'
check_out = 'null'
adults_room1 = 'null'

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
        global check_in
        check_in = request.form.get('check-in')
        print(check_in)
        global check_out
        check_out = request.form.get('check-out')
        print(check_out)
        rooms = request.form.get('rooms')
        print(rooms)
        global adults_room1
        adults_room1 = request.form.get('adult1')
        print(adults_room1)

        # search_location_id defined in helpers.py
        destinationID = search_location_id(destination)
        
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
            # print(hotels[0])
            return render_template('hotels.html', header=header, totalCount=totalCount, hotels=hotels)


@app.route("/hotels/<hotelID>", methods=['GET', 'POST'])
def show_hotel_details(hotelID):
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
    # loop through images, format size & add to list
    images_list = []
    for image in hotel_images_list:
        size = image['sizes'][0]['suffix']
        image_url = image['baseUrl'].format(size=size)
        images_list.append(image_url)
    

    return render_template('hotel_details.html', hotelID=hotel_id, hotel_name=hotel_name, hotel_stars=hotel_stars, hotel_address=hotel_address,
     hotel_price=hotel_price,amenities=amenities, what_is_around=what_is_around, tagline=tagline, freebies=freebies, hotel_rooms=hotel_rooms, images_list=images_list)
    

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