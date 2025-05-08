from django.contrib import admin
from .models import TicketOffer
from .models import Booking
from .models import Payment
from .models import Room
from .models import Guest

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name',)

    
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'room', 'check_in_date', 'check_out_date', 'total_price', 'status')

    def guest_name(self, obj):
        return obj.guest.name if obj.guest else "No Guest"
    guest_name.short_description = 'Guest Name'

admin.site.register(Payment)

admin.site.register(Room)

@admin.register(TicketOffer)
class TicketOfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price'] 
