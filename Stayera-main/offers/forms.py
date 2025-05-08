# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Booking
from .models import TicketOffer
from .models import Room  # or whatever your model is called

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name','room_number', 'room_type', 'price_per_night', 'is_occupied']

class UserUpdateForm(forms.ModelForm):
    """Form for updating user information"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """Form for updating profile information"""
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = Profile
        fields = ['birthday', 'gender', 'marital_status', 'address', 'pincode', 'state']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        
class TicketOfferForm(forms.ModelForm):
    class Meta:
        model = TicketOffer
        fields = ['title', 'description', 'image', 'price']        