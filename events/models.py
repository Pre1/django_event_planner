from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 
from django.utils import timezone
from django.urls import reverse



class Event(models.Model):

    title = models.CharField(max_length=20)
    location = models.CharField(max_length=120)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    seats = models.IntegerField()
    ticket_left = models.IntegerField()
    organized_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'event_id': self.id})

    def __str__(self):
        return self.title
    


class Booking(models.Model):
    # TODO: check if the rel. will work correctly( oneTomany vs m2m)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='booking')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    ticket_num = models.IntegerField()


    def __str__(self):
    	return "user: {} - Event: {}".format(self.user.username, self.event.title) 


