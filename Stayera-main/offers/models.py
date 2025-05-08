from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver


class TicketOffer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='offers/')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    )
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    profile_completion = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def calculate_completion_percentage(self):
        """Calculate the profile completion percentage based on filled fields"""
        total_fields = 7 
        filled_fields = 0
        
        if self.user.email:
            filled_fields += 1
        if self.user.first_name:
            filled_fields += 1
        if self.birthday:
            filled_fields += 1
        if self.gender:
            filled_fields += 1
        if self.marital_status:
            filled_fields += 1
        if self.address:
            filled_fields += 1
        if self.pincode:
            filled_fields += 1
            
        self.profile_completion = int((filled_fields / total_fields) * 100)
        self.save()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Room model
class Room(models.Model):
    ROOM_TYPES = (
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
    )
    name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    is_occupied = models.BooleanField(default=False)
    number = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.room_number} - {self.room_type} - {self.number}"


class Guest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    check_in_date = models.DateField(null=True, blank=True) 
    phone_number = models.CharField(max_length=15)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    guest = models.ForeignKey('Guest', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='confirmed')

    def __str__(self):
        return f"{self.guest.first_name} - {self.check_in_date} to {self.check_out_date}"

class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=[('Card', 'Card'), ('Cash', 'Cash')], default='Card')

    def __str__(self):
        return f"Payment #{self.id} - ${self.amount} for Booking #{self.booking.id}"
    

