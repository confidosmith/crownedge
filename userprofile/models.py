from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    pix = models.ImageField(upload_to='profile', default='profile/avatar.png', blank=True, null=True)

    def __str__(self):
        return self.user.first_name 


    class Meta:
        db_table = 'profile'
        managed = True
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    