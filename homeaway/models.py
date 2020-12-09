from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hash = db.Column(db.Text, nullable=False)
    bookings = db.relationship('Booking', backref='profile', lazy=True)

    def __init__(self, username, email, hash):
        self.username = username
        self.email = email
        self.hash = hash

class Booking(db.Model):
    __tablename__ = 'booking'
     # random booking id 
    booking_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    hotel_id = db.Column(db.Integer)
    hotel_name = db.Column(db.Text())
    city_name = db.Column(db.String(100))
    country_code = db.Column(db.String(20))
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)
    adults_room1 = db.Column(db.Integer)
    adults_room2 = db.Column(db.Integer)
    adults_room3 = db.Column(db.Integer)
    adults_room4 = db.Column(db.Integer)
    total_adults = db.Column(db.Integer)
    rooms = db.Column(db.Integer)
    room_name = db.Column(db.Text())
    total_pay = db.Column(db.Numeric)
    free_cancellation = db.Column(db.Boolean)
    cancel_before = db.Column(db.Date)
    status = db.Column(db.String(20))
    guest_name = db.Column(db.String(100))
    booked_on = db.Column(db.Date)


    def __init__(self, hotel_id, hotel_name, city_name, country_code, check_in, check_out, adults_room1, adults_room2, adults_room3, adults_room4, total_adults, rooms, room_name, total_pay, free_cancellation, cancel_before, status, guest_name, booked_on):
        self.hotel_id = hotel_id
        self.hotel_name = hotel_name
        self.city_name = city_name
        self.country_code = country_code
        self.check_in = check_in
        self.check_out = check_out
        self.adults_room1 = adults_room1
        self.adults_room2 = adults_room2
        self.adults_room3 = adults_room3
        self.adults_room4 = adults_room4
        self.total_adults = total_adults
        self.rooms = rooms
        self.room_name = room_name
        self.total_pay = total_pay
        self.free_cancellation = free_cancellation
        self.cancel_before = cancel_before
        self.status = status
        self.guest_name = guest_name
        self.booked_on = booked_on

