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
        exclude = ['organized_by',]

        widgets = {
                'date': forms.DateInput(attrs={'type': 'date'}),
                'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['ticket_num',]
        # widgets={
        #     'ticket_num': forms.NumberInput(attrs={'min': 0, 'max': booking.seats}),
        # }



class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password','first_name', 'last_name', 'email']

        widgets={
            'password': forms.PasswordInput(),
        }
