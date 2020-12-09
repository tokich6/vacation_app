# ROUTES START HERE
from homeaway import app
from datetime import date, timedelta
from flask import Flask, render_template, request, redirect, session, flash, url_for, make_response
from werkzeug.security import check_password_hash, generate_password_hash
import pdfkit

from homeaway.helpers import search_location_id, list_properties, get_hotel_details, get_hotel_photos, login_required, get_days, str_to_bool, reduce_str_len, add_together
from homeaway.models import Profile, Booking, db


@app.route("/")
@login_required
def home():
    # Set min date input for check_in & check_out
    tomorrow = date.today() + timedelta(days=1)
    day_after = date.today() + timedelta(days=2)
    # rooms = get_value(obj)
    return render_template('index.html', tomorrow=tomorrow, day_after=day_after)

@app.route("/hotels", methods=['POST'])
@login_required
def list_hotels():
    # extract parameters from the search form
    destination = request.form.get('destination')
    # need to change all global variables to session variables before production
    session['check_in'] = request.form.get('check-in')
    session['check_out'] = request.form.get('check-out')
    session['rooms'] = request.form.get('rooms')
    session['adults_room1'] = request.form.get('adult1')
    if session['rooms'] == '2':
        session['adults_room2'] = request.form.get('adult2')
        session['adults_room3'] = None
        session['adults_room4'] = None
    elif session['rooms'] == '3':
        session['adults_room2'] = request.form.get('adult2')
        session['adults_room3'] = request.form.get('adult3')
        session['adults_room4'] = None
    elif session['rooms'] == '4':
        session['adults_room2'] = request.form.get('adult2')
        session['adults_room3'] = request.form.get('adult3')
        session['adults_room4'] = request.form.get('adult4')
    else:
        session['adults_room2'] = None
        session['adults_room3'] = None
        session['adults_room4'] = None    
    
    # add_together defined in helpers.py
    session['total_adults'] = add_together(session['adults_room1'], session['adults_room2'], session['adults_room3'], session['adults_room4']) 

    sort_order = request.form.get('sort-hotels')

    # search_location_id defined in helpers.py
    destination_id = search_location_id(destination)

    if not destination:
        flash('Please type in a destination', 'error')
        return redirect("/")
    elif not session['check_in'] or not session['check_out']:
        flash('Please provide a valid check-in and check-out date', 'error')
        return redirect("/")
    else:
        # list_properties defined in helpers.py
        output = list_properties(destination_id, session['check_in'], session['check_out'], session['adults_room1'], sort_order, session['adults_room2'], session['adults_room3'], session['adults_room4'])
        # print(output)
        if output == None:
            return render_template('400.html')
        header = output['header']
        # outputs a list of hotels
        hotels = output['hotels']
        return render_template('hotels.html', header=header, hotels=hotels, sort_order=sort_order)

@app.route("/hotels/details", methods=['POST'])
@login_required
def show_hotel_details():
    # hidden input value in hotels.html
    hotel_id = request.form.get('hotel_id')
    # get_hotel_details function defined in helpers
    output_hotel_details = get_hotel_details(hotel_id, session['check_in'], session['check_out'], session['adults_room1'], session['adults_room2'], session['adults_room3'], session['adults_room4'])
    
    if output_hotel_details == None:
        return render_template('500.html')
    amenities = output_hotel_details['amenities']
    what_is_around = output_hotel_details['what_is_around']
    hotel_name = output_hotel_details['property_description']['name']
    hotel_stars = output_hotel_details['property_description']['starRating']
    hotel_address = output_hotel_details['property_description']['address']['fullAddress']
    tagline = output_hotel_details['property_description']['tagline']
    freebies = output_hotel_details['property_description']['freebies']
    hotel_price = int(output_hotel_details['property_description']['featuredPrice']['currentPrice']['plain'])
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
                           hotel_price=hotel_price, amenities=amenities, what_is_around=what_is_around, tagline=tagline, freebies=freebies, hotel_rooms=hotel_rooms, images_url_list=images_url_list)

@app.route("/booking", methods=['POST'])
@login_required
def confirm_booking():
    hotel_id = request.form.get('hotel_id')
    hotel_price = request.form.get('hotel_price')

    # contact API to check availability before final booking confirmation
    output_hotel_details = get_hotel_details(hotel_id, session['check_in'], session['check_out'], session['adults_room1'], session['adults_room2'], session['adults_room3'], session['adults_room4'])
    if output_hotel_details == None:
        return render_template('500.html')
    hotel_name = output_hotel_details['property_description']['name']
    hotel_stars = output_hotel_details['property_description']['starRating']
    hotel_address = output_hotel_details['property_description']['address']['fullAddress']
    city_name = output_hotel_details['property_description']['address']['cityName']
    country_code = output_hotel_details['property_description']['address']['countryCode']
    best_room = output_hotel_details['first_room']
    # get_days defined in helpers.py
    stay_duration = get_days(session['check_in'], session['check_out'])

    return render_template('confirm_booking.html', check_in=session['check_in'], check_out=session['check_out'], hotel_rooms=session['rooms'], total_guests=session['total_adults'],
                               hotel_id=hotel_id, hotel_name=hotel_name, hotel_stars=hotel_stars, hotel_address=hotel_address, hotel_price=hotel_price, room=best_room,
                               stay_duration=stay_duration, city_name=city_name, country_code=country_code)

@app.route("/account", methods=['GET', 'POST'])
@login_required
def your_bookings():
    today = date.today()
    free_cancellation = False
    # defaults to today's date if free cancellation is False
    cancel_before = today
    booked_on = today
    status = 'Confirmed'
    # filter by category clicked on (get request)
    btn_value = request.args.get('category', default='All')

    if request.method == 'POST':
        hotel_id = request.form.get('hotel_id')
        hotel_name = request.form.get('hotel_name')
        city_name = request.form.get('city_name')
        country_code = request.form.get('country_code')
        room_name = request.form.get('room_name')
        total_pay = request.form.get('total_pay')
        guest_name = request.form.get('guest_name')
        # str_to_bool defined in helpers.py
        free_cancellation = str_to_bool(request.form.get('free_cancellation'))
        if free_cancellation == True:
            cancel_before = reduce_str_len(request.form.get('cancel_before')) 

        # enter booking details into the database
        data = Booking(hotel_id, hotel_name, city_name, country_code, session['check_in'], session['check_out'], session['adults_room1'], session['adults_room2'], session['adults_room3'], session['adults_room4'], session['total_adults'], session['rooms'], room_name, total_pay, free_cancellation, cancel_before, status, guest_name, booked_on)
        # get current user id 
        current_user = db.session.query(Profile).filter(Profile.id == session['user_id']).first()
        # assign it to booking entry foreign key
        data.user_id = current_user.id
        db.session.add(data)
        db.session.commit()
        # get all bookings from db for current user
        bookings = db.session.query(Booking).filter(Booking.user_id == session['user_id']).order_by(Booking.check_in).all()
        flash('Your reservation is confirmed', 'success')
        return render_template('your_bookings.html', today=today, bookings=bookings)
    else:
        if btn_value == 'All':
            bookings = db.session.query(Booking).filter(Booking.user_id == session['user_id']).order_by(Booking.check_in).all()
        elif btn_value == 'Cancelled':
            bookings = db.session.query(Booking).filter(Booking.user_id == session['user_id']).filter(Booking.status == 'Cancelled').all()
        else:
            bookings = db.session.query(Booking).filter(Booking.user_id == session['user_id']).filter(Booking.status == 'Confirmed').order_by(Booking.check_in).all()
        return render_template('your_bookings.html', today=today, bookings=bookings, args=btn_value)

@app.route("/downloads", methods=['POST'])
@login_required
def generate_pdf():
    booking_id = request.form.get('booking_id')
    booking_details = db.session.query(Booking).filter(Booking.booking_id == booking_id).first()
    
    pdf_content = render_template('pdf_template.html', booking=booking_details)
    # css = ['./static/pdf.css']
    pdf = pdfkit.from_string(pdf_content, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=hotel_confirmation.pdf'
    return response

@app.route("/cancellation", methods=['POST'])
@login_required
def cancel_booking():
    today = date.today()
    booking_id = request.form.get('booking_id')
    booking_details = db.session.query(Booking).filter(Booking.booking_id == booking_id).first()
    booking_details.status = 'Cancelled'
    booking_details.total_pay = 0
    db.session.commit()

    bookings = db.session.query(Booking).filter(Booking.user_id == session['user_id']).filter(Booking.status == 'Cancelled').all()
    flash('The booking is now cancelled', 'success')
    return render_template('your_bookings.html', today=today, bookings=bookings, args='Cancelled')

@app.route("/about", methods=['GET'])
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            flash('Please provide a username', 'error')
            return redirect('/register')
        # Query database for username
        elif db.session.query(Profile).filter(Profile.username == username).count() != 0:
            flash('The username already exists, please log in if previously registered or choose a different one', 'error')
            return redirect('/register')

        email = request.form.get("email")
        if not email:
            flash('please provide an email address', 'error')
            return redirect('/register')
        elif db.session.query(Profile).filter(Profile.email == email).count() != 0:
            flash(
                'The email address you entered is already associated with an account, please log in', 'error')
            return redirect('/login')

        password = request.form.get("password")
        # Ensure password was submitted
        if not password:
            flash('must provide password', 'error')
            return redirect('/register')

        confirm_password = request.form.get("confirm-password")
        # enfure confirmation was submitted and matches the password
        if not confirm_password:
            flash('must confirm password', 'error')
            return redirect('/register')
        elif confirm_password != password:
            flash('confirm password is not a match', 'error')
            return redirect('/register')

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
    # Forget all session data
    session.clear()
    if request.method == "POST":
        # get the value of the hidden next url input
        next_url = request.form.get("next")
        # Ensure username was submitted
        if not request.form.get("username"):
            flash('must provide username', 'error')
            return render_template('login.html')

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('must provide password', 'error')
            return render_template('login.html')

        # query database for the username input
        user = db.session.query(Profile).filter(
            Profile.username == request.form.get('username')).first()

        # Ensure username exists and password is correct
        if not user or not check_password_hash(user.hash, request.form.get("password")):
            flash('invalid username and/or password, please try again', 'error')
            return render_template('login.html')

        # Remember which user has logged in
        session['user_id'] = user.id
        session['username'] = request.form['username']

        # check if we're redirecting the user to another endpoint, if not default
        if next_url:
            return redirect(next_url)
        flash('You are successfully logged in!', 'success')
        return redirect(url_for("home"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    # Forget all session data
    session.clear()
    return redirect("/")

