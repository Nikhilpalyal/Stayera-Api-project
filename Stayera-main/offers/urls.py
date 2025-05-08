from django.urls import path
from . import views

urlpatterns = [
    path('offers/', views.offers_page, name='offers_page'), 
    path('stays/', views.stays, name='stays'),      
    path('welcome/', views.welcome, name='welcome'),
    path('offer_list/', views.offer_list, name='offer_list'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('admin-booking/', views.admin_booking, name='admin_booking'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/offers/', views.dashboard_offers, name='dashboard_offers'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/<int:pk>/', views.booking_edit, name='booking_edit'),
    path('delete/<int:pk>/', views.booking_delete, name='booking_delete'),
    path('booking/add/', views.booking_add, name='booking_add'),
    path('admin/rooms/', views.admin_room, name='admin_room'),
    path('add-room/', views.add_room, name='add_room'),
    path('rooms/', views.room_list, name='room_list'),
    path('add/', views.add_room, name='add_room'),
    path('admin/rooms/', views.room_list, name='room_list'),
    path('admin/rooms/delete/<int:pk>/', views.delete_room, name='delete_room'),
    path('rooms/<int:pk>/edit/', views.edit_room, name='edit_room'),
     path('booking_page/', views.booking_page, name='booking_page'),  
    path('book/', views.handle_booking, name='handle_booking'),
    path('confirmation/', views.confirmation_page, name='confirmation_page'), ]
