from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_restful import Api, Resource
import os
import sqlite3
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_cors import CORS
import base64


app = Flask(__name__)
CORS(app)
api = Api(app)  # Initialize Flask-RESTful

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

REGISTERED_FACES_DIR = "registered_faces"
if not os.path.exists(REGISTERED_FACES_DIR):
    os.makedirs(REGISTERED_FACES_DIR)

class FaceID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

# User Model
class User(db.Model, UserMixin):  # Added UserMixin for Flask-Login
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# ContactUs model for database
class ContactUs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ContactUs {self.name} - {self.email}>"

# Payment model for database
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)
    expiry_date = db.Column(db.String(10), nullable=False)
    cvv = db.Column(db.String(3), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Payment {self.email}>'

class UPIPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    upi_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<UPIPayment {self.upi_id} - {self.amount}>"

    def to_dict(self):
        return {
            'id': self.id,
            'upi_id': self.upi_id,
            'amount': self.amount,
            'description': self.description,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }

# Configure Upload Folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database Model for Scanned IDs
class ScannedID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    extracted_text = db.Column(db.Text, nullable=False)
    face_id = db.Column(db.Integer, db.ForeignKey('face_id.id'), nullable=True)  # Link to FaceID
    face = db.relationship('FaceID', backref='scanned_ids')  # Relationship with FaceID

@app.route('/')
def home():
    about = {
        "experience": "10+",
        "title": "Why Choose Us?",
        "description": "We provide the best hospitality services with integrity and value. Stay in a home away from home and feel the your desired life with best accommodations and less costs."
    }
    collections = [
        {"image": "image/rooms.jpeg", "title": "Luxury Suites"},
        {"image": "image/luxury.jpg", "title": "Beach Resorts"},
        {"image": "image/room.jpg", "title": "Villas"},
        {"image": "image/hotel3.jpg", "title": "Family time"},
    ]
    services = [
    {
        "icon": "utensils",
        "title": "Food Service/ Food Runner",
        "description": " We ensure that hot, fresh, and delicious meals are delivered to your doorstep.Enjoy a diverse menu crafted by top chefs, featuring the finest ingredients.Savor every bite with our quick and reliable delivery service, bringing restaurant-quality meals to you."
    },
    {
        "icon": "coffee",
        "title": "Refreshment",
        "description": "From freshly brewed coffee to chilled soft drinks, we provide a range of refreshments. Quench your thirst with our carefully curated selection of beverages for every mood.Experience the perfect pairing of drinks with your favorite meals, delivered straight to you."
    },
    {
        "icon": "broom",
        "title": "HouseKeeping",
        "description": "Our housekeeping services keep your stay clean and comfortable. Our housekeeping services keep your stay clean and comfortable. Our housekeeping services keep your stay clean and comfortable.From freshly brewedhilled soft drinks, we provide a range of refreshments."
    },
    {
        "icon": "lock",
        "title": "Room Security",
        "description": "Smart keycard access, 24/7 security surveillance, and emergency support. Enjoy a safe and secure stay with advanced technology and round-the-clock protection.Your safety and peace of mind are our top priorities, ensuring a worry-free experience. Enjoy a  crafted by top chefs"
    }
]
    testimonials = [
    {
        "title": "We Loved It",
        "content": "Enjoy a delightful dining experience with our fast and efficient room service.",
        "customer": "Customer Name, Country",
        "rating": 4
    },
    {
        "title": "Comfortable Living",
        "content": "Unwind with a selection of beverages and snacks available around the clock.",
        "customer": "Customer Name, Country",
        "rating": 4
    },
    {
        "title": "Nice Place",
        "content": "Your safety is our top priority.",
        "customer": "Customer Name, Country",
        "rating": 4
    }
]
    return render_template('index.html', about=about, collections=collections, testimonials=testimonials, services=services)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/face', methods=['GET'])
def face():
    return render_template('face.html')

@app.route('/hotels')
def hotels():
    destinations = [
    {"name": "New Delhi", "image": "image/newdelhi.jpg"},
    {"name": "Bangalore", "image": "image/bangalore.jpg"},
    {"name": "Mumbai", "image": "image/chennnai.jpg"},
    {"name": "Chennai", "image": "image/mumbai.jpg"},
    {"name": "Hyderabad", "image": "image/hyderabad.jpg"},
    {"name": "Chandigarh", "image": "image/chandigarh.jpg"},
]
    
    return render_template('hotels.html', destinations=destinations)

@app.route("/room")
def room():
    hotels = [
    {
        "name": "Hotel O Lal Sai Residency",
        "location": "Andheri West, Mumbai",
        "distance": "9.9 km",
        "rating": 4.1,
        "reviews": 99,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 7469,
        "discounted_price": 1928,
        "taxes_fees": 399,
        "image": "static/lalsai.jpg",
        "badge": "Mid range"
    },
    {
        "name": "Hotel Golden Galaxy",
        "location": "Santacruz East, Mumbai",
        "distance": "6.0 km",
        "rating": 4.0,
        "reviews": 97,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 7299,
        "discounted_price": 1900,
        "taxes_fees": 399,
        "image": "static/lalsai.jpg",
        "badge": "Mid range"
    },
    {
        "name": "Hotel Ajanta",
        "location": "Juhu Beach, Mumbai",
        "distance": "3.5 km",
        "rating": 4.4,
        "reviews": 99,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 8689,
        "discounted_price": 2563,
        "taxes_fees": 399,
        "image": "static/lalsai.jpg",
        "badge": "Mid range"
    },
    {
        "name": "Hotel Marine Plaza",
        "location": "29 Marine Drive, Churchgate, Mumbai",
        "distance": "9.5 km",
        "rating": 4.9,
        "reviews": 99,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 11999,
        "discounted_price": 3999,
        "taxes_fees": 399,
        "image": "static/apartment.jpeg",
        "badge": "Mid range"
    },
    {
        "name": "Hotel Sahara Star",
        "location": "Vile Parle East, Mumbai",
        "distance": "6.5 km",
        "rating": 4.5,
        "reviews": 99,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 9999,
        "discounted_price": 2999,
        "taxes_fees": 399,
        "image": "static/lalsai.jpg",
        "badge": "Mid range"
    },
    {
        "name": "Hotel Kemps Corner",
        "location": "Kemps Corner, Mumbai",
        "distance": "9.9 km",
        "rating": 4.1,
        "reviews": 99,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 7406,
        "discounted_price": 1905,
        "taxes_fees": 399,
        "image": "static/lalsai.jpg",
        "badge": "Mid range"
    },
    {
        "name": "Taj Lands End",
        "location": "Bamdra West, Mumbai",
        "distance": "8.9 km",
        "rating": 4.7,
        "reviews": 99,
        "features": ["Free Wifi", "Geyser", "Power backup", "+ 4 more"],
        "original_price": 10969,
        "discounted_price": 2999,
        "taxes_fees": 399,
        "image": "static/golden.jpeg",
        "badge": "Mid range"
    },
]

    return render_template("room.html", hotels=hotels)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        # Validate required fields
        if not all([name, email, phone, message]):
            flash("All fields are required.", "error")
            return redirect(url_for("contact"))

        try:
            # Store the data in the database
            new_contact = ContactUs(name=name, email=email, phone=phone, message=message)
            db.session.add(new_contact)
            db.session.commit()

            flash("Your message has been sent successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "error")

        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/activity')
def activity():
    user_data = {
        "name": "Nikhil Palyal",
        "email": "nikhilpalyal6@gmail.com",
        "phone": "8264131474"
    }

    booking_data = {
        "hotel_name": "Super Townhouse Khar The Unicontinental",
        "address": "9A Rajkutir, 3rd Road, next to Doolally Taproom, next to Khar railway station, Khar West",
        "rating": "4.7 ★ (276 Ratings) • Excellent",
        "stay_details": "Sun, 16 Feb – Mon, 17 Feb | 1 Room, 1 Guest",
        "price_breakdown": {
            "room_price": 10375,
            "instant_discount": -3112,
            "coupon_discount": -3849,
            "wizard_discount": -171,
            "wizard_membership": 171,
            "oyo_money": -682,
            "payable_amount": 2732
        }
    }
    return render_template('activity.html', user=user_data, booking=booking_data)

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/upi')
def upi():
    return render_template('upi.html')

@app.route("/registerface")
def registerface():
    return render_template("registerface.html")

def init_db():
    with app.app_context():
        db.create_all()
        
        # Initialize transaction database
        with sqlite3.connect('transactions.db') as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         upi_id TEXT NOT NULL,
                         amount REAL NOT NULL,
                         description TEXT,
                         timestamp TEXT NOT NULL)''')
            conn.commit()


class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {"success": False, "message": "No data provided"}, 400

        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not all([name, email, password]):
            return {"success": False, "message": "All fields are required"}, 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"success": False, "message": "Email already exists. Please login."}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(name=name, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return {"success": True, "message": "Signup successful! Please login."}, 201
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Error: {str(e)}"}, 500

# Face Scanning Resource
class FaceScanResource(Resource):
    def post(self):
        if 'image' not in request.json:
            return {"success": False, "message": "No image data provided"}, 400

        image_data = request.json['image'].split(",")[1]  # Remove base64 header
        image_bytes = base64.b64decode(image_data)

        # Save the uploaded image temporarily
        temp_filename = f"temp_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        with open(temp_filepath, "wb") as f:
            f.write(image_bytes)

        # Placeholder for face recognition logic
        recognized_face = None
        for face in FaceID.query.all():
            # Simulate face recognition by matching file names (replace with actual face recognition logic)
            if face.name.lower() in temp_filename.lower():
                recognized_face = face
                break

        # Remove the temporary file
        os.remove(temp_filepath)

        if recognized_face:
            return {
                "success": True,
                "message": f"Welcome, {recognized_face.name}! Face recognized successfully.",
                "name": recognized_face.name
            }
        else:
            return {
                "success": False,
                "message": "Face not recognized. Please try again or register your face."
            }, 400

class FaceRegistrationResource(Resource):
    def post(self):
        try:
            data = request.json  # Get JSON data from request
            if not data or "name" not in data or "image" not in data:
                return {"success": False, "message": "Missing name or image data!"}, 400

            name = data["name"]
            image_data = data["image"].split(",")[1]  # Remove base64 header
            image_bytes = base64.b64decode(image_data)

            # Save the image with a unique filename
            image_filename = f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            image_path = os.path.join(REGISTERED_FACES_DIR, image_filename)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            # Save details in the database
            new_face = FaceID(name=name, image_path=image_path)
            db.session.add(new_face)
            db.session.commit()
            
            return {"success": True, "message": "Face registered successfully!", "image_path": image_path}
        except Exception as e:
            print("Error:", str(e))  # Print error in terminal
            return {"success": False, "message": f"An error occurred while registering face: {str(e)}"}, 500

# Contact Form Resource
class ContactResource(Resource):
    def post(self):
        try:
            # Get JSON data from the request
            data = request.get_json()
            if not data:
                return {"success": False, "message": "No data provided"}, 400

            # Extract fields from the JSON data
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            message = data.get('message')

            # Validate required fields
            if not all([name, email, phone, message]):
                return {"success": False, "message": "All fields are required"}, 400

            # Save the contact form data to the database
            new_contact = ContactUs(name=name, email=email, phone=phone, message=message)
            db.session.add(new_contact)
            db.session.commit()

            return {"success": True, "message": "Contact form submitted successfully!"}, 201

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Error submitting contact form: {str(e)}"}, 500

# OTP Resource
class OTPResource(Resource):
    def post(self):
        data = request.json
        phone = data.get("phone")
        if phone and len(phone) >= 10:
            return {"message": "OTP sent successfully!", "success": True}
        return {"message": "Invalid phone number", "success": False}

class OTPVerificationResource(Resource):
    def post(self):
        data = request.json
        otp = data.get("otp")
        if otp == "1234":  # Example OTP verification
            return {"message": "OTP verified successfully!", "success": True}
        return {"message": "Invalid OTP", "success": False}

# User Update Resource
class UserUpdateResource(Resource):
    def post(self):
        # In a real app, you'd use authentication to ensure the user can only update their own data
        try:
            data = request.get_json() or {}
            
            # Get user ID from authenticated session in a real app
            # For now, we'll just update a global variable
            global user_data
            
            if 'name' in data:
                user_data["name"] = data["name"]
            if 'email' in data:
                user_data["email"] = data["email"]
            if 'phone' in data:
                user_data["phone"] = data["phone"]
                
            return {"success": True, "message": "User details updated successfully!", "user": user_data}
        except Exception as e:
            return {"success": False, "message": f"Error updating user: {str(e)}"}, 500

# Payment Processing Resource
class PaymentResource(Resource):
    def post(self):
        try:
            # Get JSON data from request
            data = request.get_json()
            
            if not data:
                return {"success": False, "message": "No data provided"}, 400

            # Extract payment details
            email = data.get('email')
            card_number = data.get('card_number')
            expiry_date = data.get('expiry_date')
            cvv = data.get('cvv')
            payment_method = data.get('payment_method')

            # Validate required fields
            if not all([email, card_number, expiry_date, cvv, payment_method]):
                return {"success": False, "message": "All fields are required"}, 400

            # Basic validation
            if not 13 <= len(str(card_number)) <= 16:
                return {"success": False, "message": "Invalid card number"}, 400

            if len(str(cvv)) not in [3, 4]:
                return {"success": False, "message": "Invalid CVV"}, 400

            # Create new payment record
            new_payment = Payment(
                email=email,
                card_number=card_number,
                expiry_date=expiry_date,
                cvv=cvv,
                payment_method=payment_method
            )

            # Save to database
            db.session.add(new_payment)
            db.session.commit()

            return {
                "success": True,
                "message": "Payment processed successfully",
                "payment_id": new_payment.id
            }

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Error processing payment: {str(e)}"}, 500
    
    def get(self):
        try:
            payments = Payment.query.order_by(Payment.created_at.desc()).all()
            return {
                "success": True,
                "payments": [{
                    "id": p.id,
                    "email": p.email,
                    "payment_method": p.payment_method,
                    "created_at": p.created_at.strftime('%Y-%m-%d %H:%M:%S')
                } for p in payments]
            }
        except Exception as e:
            return {"success": False, "message": f"Error retrieving payments: {str(e)}"}, 500

# UPI Payment Resource
class UPIPaymentResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"success": False, "message": "No data provided"}, 400

            upi_id = data.get('upi_id')
            amount = data.get('amount')
            description = data.get('description', '')

            # Validate required fields
            if not upi_id or not amount:
                return {"success": False, "message": "UPI ID and amount are required"}, 400

            # Validate UPI ID format
            if '@' not in upi_id:
                return {"success": False, "message": "Invalid UPI ID format"}, 400

            # Validate amount
            try:
                amount = float(amount)
                if amount <= 0:
                    return {"success": False, "message": "Amount must be greater than zero"}, 400
            except ValueError:
                return {"success": False, "message": "Invalid amount"}, 400

            # Store in database
            new_payment = UPIPayment(upi_id=upi_id, amount=amount, description=description)
            db.session.add(new_payment)
            db.session.commit()

            return {
                "success": True,
                "message": "UPI payment stored successfully",
                "payment_id": new_payment.id
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Error storing UPI payment: {str(e)}"}, 500

    def get(self):
        try:
            payments = UPIPayment.query.order_by(UPIPayment.timestamp.desc()).all()
            return {"success": True, "payments": [payment.to_dict() for payment in payments]}, 200
        except Exception as e:
            return {"success": False, "message": f"Error fetching payments: {str(e)}"}, 500

# Transactions Resource
class TransactionsResource(Resource):
    def get(self):
        try:
            with sqlite3.connect('transactions.db') as conn:
                c = conn.cursor()
                c.execute('SELECT * FROM transactions ORDER BY timestamp DESC')
                transactions = c.fetchall()

            formatted_transactions = [
                {
                    'id': t[0],
                    'upi_id': t[1],
                    'amount': t[2],
                    'description': t[3],
                    'timestamp': t[4]
                } for t in transactions
            ]
            return {"success": True, "transactions": formatted_transactions}
        except Exception as e:
            return {"success": False, "message": f"Error fetching transactions: {str(e)}"}, 500

# Login Resource
class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"success": False, "message": "No data provided"}, 400
                
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return {"success": False, "message": "Email and password are required"}, 400
                
            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return {
                    "success": True, 
                    "message": f"Welcome {user.name}! Login successful.",
                    "user_id": user.id,
                    "name": user.name,
                    "email": user.email
                }
            
            return {"success": False, "message": "Invalid email or password."}, 401
            
        except Exception as e:
            return {"success": False, "message": f"Login error: {str(e)}"}, 500

# Logout Resource
class LogoutResource(Resource):
    @login_required
    def post(self):
        try:
            logout_user()
            return {"success": True, "message": "Logged out successfully."}
        except Exception as e:
            return {"success": False, "message": f"Logout error: {str(e)}"}, 500

api.add_resource(SignupResource, '/api/signup')
api.add_resource(FaceScanResource, '/api/scan-id')
api.add_resource(FaceRegistrationResource, '/api/register-face')
api.add_resource(ContactResource, '/api/contact')
api.add_resource(OTPResource, '/api/send_otp')
api.add_resource(OTPVerificationResource, '/api/verify_otp')
api.add_resource(UserUpdateResource, '/api/update_user')
api.add_resource(PaymentResource, '/api/payment')
api.add_resource(UPIPaymentResource, '/api/upi_payment')
api.add_resource(TransactionsResource, '/api/transactions')
api.add_resource(LoginResource, '/api/login')
api.add_resource(LogoutResource, '/api/logout')


# Run Server
if __name__ == "__main__":
    init_db()
    app.run(debug=True)