from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, role='user'):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, name, password=None):
        user = self.create_user(email=email, name=name, password=password, role='admin')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='user')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.role})"
    

class RegisteredFace(models.Model):
    image = models.ImageField(upload_to='faces/')
    created_at = models.DateTimeField(auto_now_add=True)




# class Payment(models.Model):
    # email = models.EmailField()
    # card_number = models.CharField(max_length=16)
    # expiry_date = models.CharField(max_length=5)
    # cvv = models.CharField(max_length=4)
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    # created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"{self.email} - {self.amount}"


class Payment(models.Model):
    upi_id = models.CharField(max_length=100)  # UPI ID of the user
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    description = models.TextField(blank=True, null=True)  # Optional payment description
    payment_method = models.CharField(max_length=20, default="UPI")  # Payment method (default is UPI)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the payment

    def __str__(self):
        return f"{self.upi_id} - ₹{self.amount} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

from django.db import models

class ContactUs(models.Model):
    name = models.CharField(max_length=150)  # Name of the user
    email = models.EmailField()  # Email of the user
    phone = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    message = models.TextField()  # Message from the user
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the message was created

    def __str__(self):
        return f"{self.name} - {self.email}"