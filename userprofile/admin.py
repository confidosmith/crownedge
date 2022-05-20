from django.contrib import admin
from . models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'username', 'email', 'phone', 'state','pix']

admin.site.register(Profile,ProfileAdmin)