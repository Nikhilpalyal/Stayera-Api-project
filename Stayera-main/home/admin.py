from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('upi_id', 'amount', 'payment_method', 'created_at')
    search_fields = ('upi_id', 'payment_method')