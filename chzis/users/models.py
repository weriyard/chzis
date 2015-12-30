from __future__ import unicode_literals
import datetime

from django.db import models


class People(models.Model):
    GENDER = (
        ('M', 'male'),
        ('F', 'female'),
    )

    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    system_account = models.BooleanField(default=False)
    perms = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=1, choices=GENDER, default='male')
    last_modification = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return "{lastname} {firstname}".format(lastname=self.lastname, firstname=self.firstname)

    class Meta:
        ordering = ['lastname', 'firstname']




