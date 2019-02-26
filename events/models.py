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
    poster = models.ImageField(upload_to='event_posters', null=True)
    organized_by = models.ForeignKey(
    	User,
    	on_delete=models.CASCADE,
    	default=1,
    	related_name='organizer')

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'event_id': self.id})

    def tickets_left(self):
    	total_tickets = 0

    	bookings = self.booking.all().values_list('ticket_num', flat = True)
    	for ticket in bookings:
    		total_tickets += ticket
    	return self.seats - total_tickets


    def __str__(self):
        return self.title
    

class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='booking')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking')
    timestamp = models.DateTimeField(auto_now_add=True)
    ticket_num = models.IntegerField()


    def __str__(self):
    	return "user: {} - Event: {}".format(self.user.username, self.event.title) 


