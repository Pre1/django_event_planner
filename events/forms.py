from django import forms
from django.contrib.auth.models import User
from .models import Booking, Event


class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['ticket_left', 'organized_by']

        widgets = {
                # 'date': forms.DateInput(attrs={'type': 'date'}),
                'date': forms.DateInput(format='%b %d, %Y'), # oct 12, 2019
                # 'time': forms.DateInput(attrs={'type': 'time'}),
                'time': forms.TimeInput(format='%I: %M %p'), # 12hr: m am/pm
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['ticket_num',]
