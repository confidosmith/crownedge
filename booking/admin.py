from django.contrib import admin
from . models import *

# Register your models here.

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user','room','display', 'room_no','booking_code','booking_date','checkin', 'checkout', 'no_days', 'amount','paid','available','del_booking','future','checkout_update']
    readonly_fields = ['user', 'room', 'room_no', 'booking_code', 'checkin', 'checkout', 'no_days', 'amount', 'paid','available']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','first_name','last_name','amount','paid','phone','pay_code','payment_date','admin_update','admin_note']
    readonly_fields = ['user','first_name','last_name','amount','paid','phone','pay_code']


