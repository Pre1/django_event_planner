from django.db import models
from django.contrib.auth.models import User



class Event(models.Model):

    title = models.CharField(max_length=20)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    seats = models.IntegerField()
    ticket_left = models.IntegerField()
    organized_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def get_absolute_url(self):
		return reverse('event-detail', kwargs={'event_id': self.id})

    def __str__(self):
        self.title
    


class Booking(models.Model):
	# TODO: check if the rel. will work correctly( oneTomany vs m2m)
	event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='booking')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking')



