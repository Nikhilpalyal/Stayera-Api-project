from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_backends, login
from .models import CustomUser
import requests
import random
import requests
import base64
from .models import RegisteredFace
from .models import Payment  # Ensure you have a Payment model in your models.py


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def hotels(request):
    if not request.user.is_authenticated:
        return redirect('form')
    return render(request, 'hotels.html') 

def form(request):
    if request.method == 'POST':
        print("Form submitted with data:", request.POST)

        # SIGNUP
        if 'name' in request.POST and 'confirm_password' in request.POST:
            try:
                name = request.POST['name']
                email = request.POST['email']
                password = request.POST['password']
                confirm_password = request.POST['confirm_password']
                role = request.POST['role']

                print(f"Processing signup: {name}, {email}, {role}")
                if password != confirm_password:
                    messages.error(request, "Passwords do not match")
                    return render(request, 'form.html')  # Avoid redirect loop

                api_url = "http://127.0.0.1:5000/api/signup"
                response = requests.post(api_url, json={
                    "name": name,
                    "email": email,
                    "password": password,
                    "role": role
                })

                if response.status_code == 200:
                    api_response = response.json()
                    if api_response.get("success"):
                        user = CustomUser.objects.create_user(email=email, name=name, password=password, role=role)
                        user.backend = get_backends()[0].__module__ + '.' + get_backends()[0].__class__.__name__
                        auth_login(request, user)
                        messages.success(request, "Registered successfully.")
                        return redirect('hotels')
                    else:
                        messages.error(request, api_response.get("message", "Registration failed"))
                        return render(request, 'form.html')
                else:
                    print(f"Flask API error: {response.status_code}, {response.text}")
                    messages.error(request, "Error connecting to the registration service")
                    return render(request, 'hotels.html')
            except Exception as e:
                print(f"Registration error: {str(e)}")
                messages.error(request, f"Registration error: {str(e)}")
                return render(request, 'form.html')

        # LOGIN
        else:
            try:
                email = request.POST['email']
                password = request.POST['password']
                print(f"Processing login: {email}")

                api_url = "http://127.0.0.1:5000/api/login"
                response = requests.post(api_url, json={
                    "email": email,
                    "password": password
                })

                if response.status_code == 200:
                    user_data = response.json()
                    if user_data.get("success") and "user" in user_data:
                        user_info = user_data["user"]
                        print(f"User authenticated: {user_info['email']}, role: {user_info['role']}")

                        user, created = CustomUser.objects.get_or_create(email=user_info['email'])
                        if created:
                            user.name = user_info['name']
                            user.role = user_info['role']
                            user.set_password(password)
                            user.save()

                        # Authenticate user (ensure password is valid if already exists)
                        if not created:
                            user = authenticate(request, email=email, password=password)
                            if user is None:
                                messages.error(request, "Invalid credentials")
                                return render(request, 'form.html')

                        auth_login(request, user)

                        if user.role == 'admin':
                            return redirect('offers:admin_dashboard')
                        else:
                            return redirect('hotels')
                    else:
                        messages.error(request, "Invalid credentials")
                        return render(request, 'form.html')
                else:
                    print(f"Flask API error: {response.status_code}, {response.text}")
                    messages.error(request, "Login error: Unable to authenticate")
                    return render(request, 'form.html')
            except Exception as e:
                print(f"Login error: {str(e)}")
                messages.error(request, f"Login error: {str(e)}")
                return render(request, 'form.html')

    # GET request: render the registration/login form
    return render(request, 'form.html')

def contact(request):
    return render(request, 'contact.html')

def booking(request):
    return render(request, 'booking.html')

def base(request):
    return render(request, 'base.html')


def payment(request):
    if request.method == 'POST':
        try:
            # Extract data from the form
            email = request.POST.get('email')
            card_number = request.POST.get('card_number')
            expiry_date = request.POST.get('expiry_date')
            cvv = request.POST.get('cvv')
            amount = request.POST.get('amount')

            # Validate required fields
            if not all([email, card_number, expiry_date, cvv, amount]):
                messages.error(request, "All fields are required for card payment.")
                return redirect('card_payment')

            # Save payment data to the database
            payment = Payment(
                email=email,
                card_number=card_number,
                expiry_date=expiry_date,
                cvv=cvv,
                amount=amount,
                payment_method="Card"
            )
            payment.save()

            messages.success(request, "Card payment details saved successfully.")
            return redirect('payment_receipt')  # Redirect to a receipt or confirmation page
        except Exception as e:
            messages.error(request, f"Error saving card payment: {str(e)}")
            return redirect('card_payment')

    return render(request, 'payment.html')
def face(request):
    return render(request, 'face.html')

@csrf_exempt
def registerface(request):
    if request.method == 'POST':
        try:
            # Extract the base64 image data from the request
            image_data = request.POST.get('image_data')
            if not image_data:
                print("Error: No image data provided")  # Debugging
                return JsonResponse({'status': 'error', 'message': 'No image data provided'}, status=400)

            print(f"Received image data: {image_data[:50]}...")  # Print the first 50 characters for debugging

            # Send the image data to the Flask API for face registration
            api_url = "http://127.0.0.1:5000/api/faces"
            print(f"Sending data to Flask API: {api_url}")
            response = requests.post(api_url, json={'image_data': image_data})

            print(f"Flask API Response: {response.status_code}, {response.text}")  # Debugging Flask API response

            if response.status_code == 200:
                api_response = response.json()
                if api_response.get('status') == 'success':
                    return JsonResponse({'status': 'success', 'message': api_response.get('message', 'Face registered successfully')}, status=200)
                else:
                    return JsonResponse({'status': 'error', 'message': api_response.get('message', 'Unknown error')}, status=400)
            else:
                print(f"Flask API error: {response.status_code}, {response.text}")
                return JsonResponse({'status': 'error', 'message': 'Failed to register face via Flask API'}, status=500)
        except Exception as e:
            print(f"Error in registerface: {str(e)}")  # Debugging
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return render(request, 'registerface.html')

def room(request):
    return render(request, 'room.html')

def upi_payment(request):
    if request.method == 'POST':
        try:
            # Extract data from the form
            upi_id = request.POST.get('upiId')
            amount = request.POST.get('amount')
            description = request.POST.get('description')

            # Validate required fields
            if not all([upi_id, amount]):
                messages.error(request, "UPI ID and Amount are required.")
                # Check if the Payment model exists and save the data
                if Payment.objects.exists():
                    payment = Payment(
                        email=upi_id,  # Using email field to store UPI ID
                        amount=amount,  # Storing the amount in the amount field
                        description=description,  # Storing the description
                        payment_method="UPI"
                    )
                    payment.save()
                    messages.success(request, "Payment details saved successfully.")
                else:
                    messages.error(request, "Payment model does not exist in the database.")
                
                return redirect('upi_payment')

            # Save payment data to the database
            payment = Payment(
                email=upi_id,  # Using email field to store UPI ID
                amount=amount,  # Storing the amount in the amount field
                description=description,  # Storing the description
                payment_method="UPI"
            )
            payment.save()

            messages.success(request, "Payment details saved successfully.")
            return redirect('upi_payment')  # Redirect to the same page or a confirmation page
        except Exception as e:
            messages.error(request, f"Error saving payment: {str(e)}")
            return redirect('upi_payment')

    return render(request, 'upi.html')

def send_otp(request):
    if request.method == 'POST':
        otp = random.randint(1000, 9999)
        print(f"OTP sent: {otp}")
        request.session['otp'] = otp 
        return JsonResponse({'status': 'OTP sent'})
    return JsonResponse({'status': 'Invalid request'})

def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        real_otp = str(request.session.get('otp'))
        if user_otp == real_otp:
            return JsonResponse({'status': 'OTP verified'})
        else:
            return JsonResponse({'status': 'OTP incorrect'})
    return JsonResponse({'status': 'Invalid request'})


def booking_view(request):
    if request.method == 'POST':
        request.session['user'] = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
        }

        request.session['booking'] = {
            'hotel_name': request.POST.get('hotel_name'),
            'address': request.POST.get('address'),
            'rating': request.POST.get('rating'),
            'stay_details': request.POST.get('stay_details'),
            'price_breakdown_readable': {
                'Room Price': request.POST.get('room_price'),
                'Taxes': request.POST.get('taxes'),
                'Total': request.POST.get('total_price')
            }
        }

        return redirect('activity')  

    return render(request, 'booking.html')


def booking_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        request.session['user'] = {
            'name': name,
            'email': email,
            'phone': phone
        }

        return redirect('activity') 
def activity_page(request):
    user = request.session.get('user', {})
    booking = request.session.get('booking', {})  

    return render(request, 'activity.html', {
        'user': user,
        'booking': booking
    })

transactions = []

@csrf_exempt
def make_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            upi_id = data.get('upi_id')
            amount = float(data.get('amount'))
            description = data.get('description', '')

            if not upi_id or amount <= 0:
                return JsonResponse({'error': 'Invalid input'}, status=400)

            transaction = {
                'upi_id': upi_id,
                'amount': amount,
                'description': description,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # ✅ this is perfect now
            }

            transactions.insert(0, transaction)  # store latest first
            return JsonResponse({'message': 'Payment successful'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_transactions(request):
    return JsonResponse(transactions, safe=False)


def activity(request):
    user = request.session.get('user', {})
    booking = request.session.get('booking', {})

    context = {
        'name': user.get('name'),
        'email': user.get('email'),
        'phone': user.get('phone'),
        'hotel_name': booking.get('hotel_name'),
        'address': booking.get('address'),
        'rating': booking.get('rating'),
        'stay_details': booking.get('stay_details'),
        'room_price': booking.get('price_breakdown_readable', {}).get('Room Price'),
        'taxes': booking.get('price_breakdown_readable', {}).get('Taxes'),
        'total_price': booking.get('price_breakdown_readable', {}).get('Total'),
    }

    return render(request, 'activity.html', context)

def activity(request):
    user = request.session.get('user', {})
    booking = request.session.get('booking', {})

    context = {
        'user': user,
        'booking': booking,
    }
    return render(request, 'activity.html', context)
def payment_receipt(request):
    if request.method == "POST":
        email = request.POST.get("email")
        card_number = request.POST.get("card-number")
        expiry_date = request.POST.get("expiry-date")
        cvv = request.POST.get("cvv")

        receipt_data = {
            "email": email,
            "hotel": "Hotel Golden Galaxy",
            "plan": "Gold Membership",
            "amount": "Rs.1735",
            "date": datetime.now(),
            "payment_method": "Credit Card"
        }

        return render(request, "receipt.html", receipt_data)
    return HttpResponse("Invalid request")




def adminpanel(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        return redirect('form')
    return render(request, 'admin_dashboard.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'forgot_password.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = '/forgot-password/done/'


@csrf_exempt
def api_payment(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                email = data.get('email')
                card_number = data.get('card_number')
                expiry_date = data.get('expiry_date')
                cvv = data.get('cvv')
                amount = data.get('amount')
                payment_method = data.get('payment_method', 'Card')

                # Validate required fields
                if not all([email, card_number, expiry_date, cvv, amount]):
                    return JsonResponse({'status': 'error', 'message': 'All fields are required'}, status=400)

                # Save payment data to the database
                payment = Payment(
                    email=email,
                    card_number=card_number,
                    expiry_date=expiry_date,
                    cvv=cvv,
                    amount=amount,
                    payment_method=payment_method
                )
                payment.save()

                return JsonResponse({'status': 'success', 'message': 'Payment processed successfully'}, status=200)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def fetch_payment_api(request):
    if request.method == 'GET':
        try:
            # Fetch payment data from the external API
            api_url = "http://127.0.0.1:5000/api/payments"
            response = requests.get(api_url)

            if response.status_code == 200:
                payment_data = response.json()
                return JsonResponse({'status': 'success', 'data': payment_data}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to fetch payment data'}, status=response.status_code)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def fetch_and_display_payments(request):
    if request.method == 'GET':
        try:
            # Fetch payment data from the Flask API
            api_url = "http://127.0.0.1:5000/api/payments"
            response = requests.get(api_url)

            if response.status_code == 200:
                payment_data = response.json()
                return render(request, 'payments.html', {'payments': payment_data})
            else:
                messages.error(request, "Failed to fetch payment data from Flask API.")
                return redirect('adminpanel')
        except Exception as e:
            messages.error(request, f"Error fetching payment data: {str(e)}")
            return redirect('adminpanel')

    return HttpResponse("Invalid request method", status=405)



def upi_payment_to_flask(request):
    if request.method == 'POST':
            try:
                # Extract data from the form
                upi_id = request.POST.get('upiId')
                amount = request.POST.get('amount')
                description = request.POST.get('description', '')

                # Validate required fields
                if not all([upi_id, amount]):
                    messages.error(request, "UPI ID and Amount are required.")
                    return redirect('upi_payment')

                # Send data to the Flask API
                api_url = "http://127.0.0.1:5000/api/upi_payment"
                payload = {
                    'upi_id': upi_id,
                    'amount': amount,
                    'description': description
                }
                response = requests.post(api_url, json=payload)

                if response.status_code == 200:
                    api_response = response.json()
                    if api_response.get('status') == 'success':
                        messages.success(request, "UPI payment processed successfully.")
                    else:
                        messages.error(request, api_response.get('message', 'Payment failed.'))
                else:
                    messages.error(request, "Failed to process payment via Flask API.")
            except Exception as e:
                messages.error(request, f"Error processing payment: {str(e)}")
            return redirect('upi_payment')

    return render(request, 'upi.html')