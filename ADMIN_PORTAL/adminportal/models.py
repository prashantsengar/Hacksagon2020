from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from fb import db as dbreference

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(max_length=20, blank=False)
    last_name = models.TextField(max_length=20, blank=False)
    designation = models.TextField(max_length=20, blank=False)
    email = models.EmailField(max_length=30, blank=False, unique=True)
    phone = models.IntegerField(max_length=10, unique=True)
    ID = models.TextField(max_length=20, unique=True)
    lat = 29.123
    long = 72.132

    def save(self):
        print('clled')
        super().save(self)
        requests.get('https://SIHapi.psproject.repl.co/register', args={'email':self.email, 'lat':self.lat, 'long':self.long})

        dbreference.child('sos_location').child(self.email.replace('@','%').replace('.','%').set({
            'email':self.email,
            'location':{'lat':self.lat, 'long':self.long},
            'name':self.first_name+self.last_name,
            'ID':self.ID,
            'phone':self.phone
        }))

