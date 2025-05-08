from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TicketOffer, Profile  # Import Profile from your own models
from datetime import datetime
from .models import TicketOffer, Room
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.http import HttpResponse
from offers.models import Booking, Guest, Payment, Room
from datetime import date
from django.db.models import Sum
from offers.forms import BookingForm
from django.utils.dateparse import parse_datetime
from .models import TicketOffer
from .forms import TicketOfferForm
from django.contrib.auth import logout
import pprint
from .forms import RoomForm
from django.urls import reverse

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

from .forms import ProfileUpdateForm, UserUpdateForm

def offers_page(request):
    images = [
        'images/offer1.webp',
        'images/offer2.webp',
        'images/offer3.jpeg',
        'images/offer4.jpeg',
        'images/room.jpg'
    ]  
    return render(request, 'offers.html', {'images': images})

def stays(request):
    return render(request, 'stays.html')

def welcome(request):
    return render(request, 'welcome.html')

def offer_list(request):
    offers = TicketOffer.objects.all()
    return render(request, 'offer_list.html', {'offers': offers})


@login_required
def profile_view(request):
    """Display user profile page"""
    Profile.objects.get_or_create(user=request.user)
    
    try:
        request.user.profile.calculate_completion_percentage()
    except AttributeError:
        pass
    
    context = {
        'user': request.user,
        'completion_percentage': getattr(request.user.profile, 'profile_completion', 0)
    }
    
    return render(request, 'userProfile.html', context)

@login_required
def edit_profile(request):
    """Edit user profile information"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            request.user.refresh_from_db()  
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('offers:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'editProfile.html', context)

def offer_list(request):
    offers = TicketOffer.objects.all()
    return render(request, 'offer_list.html', {'offers': offers})

def admin_booking(request):
    bookings = Booking.objects.all().order_by('-id')
    total_bookings = Booking.objects.count()
    guests_today = Guest.objects.filter(check_in_date=date.today()).count()
    revenue = Payment.objects.filter(payment_date__month=date.today().month).aggregate(Sum('amount'))['amount__sum'] or 0
    total_rooms = Room.objects.count()
    occupied_rooms = Room.objects.filter(is_occupied=True).count()
    occupancy_rate = round((occupied_rooms / total_rooms) * 100) if total_rooms else 0
    bookings = Booking.objects.select_related('guest', 'room')
    bookings = Booking.objects.all()

    latest_bookings = Booking.objects.select_related('guest', 'room').order_by('-check_in_date')[:10]

    context = {
        'total_bookings': total_bookings,
        'guests_today': guests_today,
        'revenue': revenue,
        'occupancy_rate': occupancy_rate,
        'bookings': latest_bookings,
    }

    return render(request, 'admin_booking.html', context)

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def admin_room(request):
    Number = Room.objects.count()
    Is_occupied = Room.objects.filter(is_occupied=True).count()
    Is_available = Room.objects.filter(is_occupied=False).count()
    Occupancy_rate = round((Is_occupied / Number) * 100) if Number else 0

    room_details = Room.objects.all().select_related()

    context = {
        'Number': Number,
        'Is_occupied': Is_occupied,
        'Is_available': Is_available,
        'Occupancy_rate': Occupancy_rate,
        'room_details': room_details,
    }

    return render(request, 'admin_room.html', context)

 
def dashboard(request):
    bookings = Booking.objects.select_related('guest', 'room').all()    
    print("DEBUG BOOKINGS:", bookings)  
    for b in bookings:
        print(b.guest_name, b.room, b.check_in, b.check_out, b.status) 
        return render(request, 'dashboard.html', {'bookings': bookings})


def dashboard_offers(request):
    offers = TicketOffer.objects.all()
    return render(request, 'dashboard/offers_list.html', {'offers': offers})

def booking_add(request):
     if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('offers:admin_booking')  
        else:
            print("Form Errors:", form.errors)
     else:
        form = BookingForm()
     return render(request, 'booking_add.html', {'form': form})

def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    form = BookingForm(request.POST or None, instance=booking)
    if form.is_valid():
        form.save()
        return redirect('offers:admin_dashboard')
    return render(request, 'edit_booking.html', {'form': form})

def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    return redirect('offers:admin_dashboard')


def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('offers:admin_room')  
    else:
        form = RoomForm()
    return render(request, 'add_room.html', {'form': form})


def room_dashboard(request):
    total_rooms = Room.objects.count()
    occupied_rooms = Room.objects.filter(is_occupied=True).count()
    available_rooms = Room.objects.filter(is_occupied=False).count()
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0

    context = {
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'available_rooms': available_rooms,
        'occupancy_rate': round(occupancy_rate, 2)
    }

    return render(request, 'admin_room.html', context)

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('offers:admin_room')  
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'edit_room.html', {
        'form': form,
        'action': 'Edit'
    })

def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('offers:admin_room')  
    return render(request, 'delete_room.html', {'room': room})



def handle_booking(request):
    if request.method == 'POST':
        first = request.POST['first_name']
        last = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        
        context = {
            'first_name': first,
            'last_name': last,
            'email': email,
            'phone': phone
        }

        return render(request, 'confirmation_page.html', context)
    
    return HttpResponse("Invalid request", status=400)

def booking_page(request):
    if request.method == 'POST':
        # You can grab the form data like this:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Do something with the data (e.g., save to DB)

        # Redirect to confirmation page
        return redirect(reverse('offers:confirmation_page'))

    return render(request, 'booking_page.html') 

def confirmation_page(request):
    return render(request, 'confirmation_page.html')
