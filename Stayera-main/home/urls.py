from django.urls import path
from . import views
from .views import CustomPasswordResetView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),  # About page
    path('activity/', views.activity, name='activity'),
    path('hotels/', views.hotels, name='hotels'),  # Hotels page
    path('contact/', views.contact, name='contact'),
    path('booking/', views.booking, name='booking'),  # Booking page
    path('payment/', views.payment, name='payment'),  # Payment page
    path('registerface/', views.registerface, name='registerface'),  
    path('room/', views.room, name='room'),  # Room page
    path('form/', views.form, name='form'),  # Form page
    path('face/', views.face, name='face'),  
    path('base/', views.base, name='base'),  
    path('upi/', views.upi_payment, name='upi'),  
    path('booking/', views.booking, name='booking'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('upi-payment/', views.upi_payment, name='upi'),
    path('make_payment', views.make_payment, name='make_payment'),
    path('get_transactions', views.get_transactions, name='get_transactions'),
    path('payment/receipt/', views.payment_receipt, name='payment_receipt'),
    path('adminpanel/', views.adminpanel, name='adminpanel'),  # Changed from 'admin_panel'
    path('forgot-password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='forgot_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

]
