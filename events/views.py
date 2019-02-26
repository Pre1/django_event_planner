from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm ,BookingForm
from django.contrib import messages
from django.http import Http404
from django.db.models import Q

from .models import Booking, Event

import datetime

def home(request):
	events = Event.objects.all()[:10]
	context = {
		"events": events 
	}
	return render(request, 'home.html', context)


def list_event(request):
	upcoming_dates = datetime.datetime.today().date()
	events = Event.objects.all().filter(date__gte = upcoming_dates)
	query = request.GET.get('search')
	if query:
		events = events.filter(
				Q(title__icontains=query)|
				Q(description__icontains=query)|
				Q(organized_by__username__icontains=query)
			).distinct()

	context = {
		"events": events 
	}
	
	return render(request, 'list.html', context)


def dashboard_event(request):
	

	events_orgs = Event.objects.filter(organized_by=request.user)
	events_attend = Booking.objects.filter(user=request.user)
	
	context = {
		'events_orgs': events_orgs,
		'events_attend': events_attend,
	}


	return  render(request, 'dashboard.html', context)



def event_detail(request , event_id):
	event_obj = Event.objects.get(id=event_id)
	booking_obj = Booking.objects.filter(event=event_obj)
	form = BookingForm()
	

	# ============ POSTING ============  
	if request.method == "POST":
		form = BookingForm(request.POST)
		if event_obj.ticket_left == 0:
			messages.warning(request, "No tickets left. Plsease Booked another Event")
			return redirect('list-event')
		if form.is_valid():
			booking_obj = form.save(commit=False)
			booking_obj.event = event_obj
			booking_obj.user = request.user
			
			if booking_obj.ticket_num > event_obj.ticket_left:
				messages.warning(request, "the number of tickets exceeded the limit")
				return redirect(event_obj)

			event_obj.ticket_left -= booking_obj.ticket_num 
			booking_obj.event.save()
			booking_obj.save()
			return redirect('event-detail', event_id)
	# ============ POSTING ============ 

	context = {
		"form":form,
		"event" : event_obj,
		"booking": booking_obj,
	}
	return render(request, 'detail.html', context)


def event_create(request):
	if request.user.is_anonymous:
		return redirect('login')
	form = EventForm()
	if request.method == "POST":
		form = EventForm(request.POST)
		if form.is_valid():
			event_obj = form.save(commit=False)
			event_obj.organized_by = request.user
			event_obj.ticket_left = event_obj.seats
			event_obj.save()
			return redirect('home')
	context = {
		"form":form,
	}
	return render(request, 'create.html', context)


def booking_event(request, event_id):
	form = BookingForm()
	event_obj = Event.objects.get(id=event_id)
	if request.method == "POST":
		form = BookingForm(request.POST)
		if form.is_valid():
			booking_obj = form.save(commit=False)
			booking_obj.event = event_obj
			booking_obj.user = request.user
			if booking_obj.ticket_num > event_obj.ticket_left:
				messages.warning(request, "the number of tickets exceeded the limit")
				return redirect(event_obj)

			event_obj.ticket_left -= booking_obj.ticket_num 
			booking_obj.event.save()
			booking_obj.save()
			return redirect('event-detail', event_id)
	context = {
		"form":form,
		"event": event_obj,
	}
	return render(request, 'booking.html', context)


class Signup(View):
	form_class = UserSignup
	template_name = 'signup.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(user.password)
			user.save()
			messages.success(request, "You have successfully signed up.")
			login(request, user)
			return redirect("home")
		messages.warning(request, form.errors)
		return redirect("signup")


class Login(View):
	form_class = UserLogin
	template_name = 'login.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				messages.success(request, "Welcome Back!")
				return redirect('dashboard')
			messages.warning(request, "Wrong email/password combination. Please try again.")
			return redirect("login")
		messages.warning(request, form.errors)
		return redirect("login")
	form_class = UserLogin
	template_name = 'login.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class()
		return render(request, self.template_name, {'form': form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				messages.success(request, "Welcome Back!")
				# if request.user.
				return redirect('dashboard')
			messages.warning(request, "Wrong email/password combination. Please try again.")
			return redirect("login")
		messages.warning(request, form.errors)
		return redirect("login")

class Logout(View):
	def get(self, request, *args, **kwargs):
		logout(request)
		messages.success(request, "You have successfully logged out.")
		return redirect("login")


def update_event(request, event_id):
	event = Event.objects.get(id=event_id)

	if not(request.user.is_staff or request.user == event.organized_by):
		return redirect('login')

	event_form = EventForm(instance=event)
	if request.method == 'POST':
		print('update - POST')
		event_form = EventForm(request.POST, instance=event)
		if form.is_valid():
			print('update - is_valid')
			form.save()
			return redirect('event-detail', event_id)

	context = {
		'form': event_form,
		'event': event
	}

	return  render(request, 'update.html', context)


