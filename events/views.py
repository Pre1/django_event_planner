from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, BookingForm, ProfileForm
from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Booking, Event, User, Follow

def home(request):
	today = datetime.today().date()
	events = Event.objects.filter(date__gte = today)[:10]
	context = {
		"events": events 
	}
	return render(request, 'home.html', context)


def list_event(request):
	today = datetime.today().date()
	events = Event.objects.filter(date__gte = today)
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

	events_orgs = request.user.organizer.all()
	current_date = datetime.today().date()
	events_attend = request.user.booking.filter(event__date__lte = current_date)
	events_upcoming = request.user.booking.filter(event__date__gte= current_date)

	context = {
		'events_orgs': events_orgs,
		'events_attend': events_attend,
		'events_upcoming': events_upcoming,
	}


	return  render(request, 'dashboard.html', context)

def profile(request):
	user_obj = User.objects.get(id=request.user.id)
	user_events = user_obj.organizer.all()
	
	f1 = Follow.objects.filter(follower=user_obj).values_list('follower', flat=True)
	f2 = Follow.objects.filter(following=user_obj).values_list('following', flat=True)
	

	# followers = user_obj.follower.all().values_list('follower', flat=True)
	# following = user_obj.following.all()
	
	# filter_follow = following.filter(follower=user_obj).values_list('following', flat=True)
	
	# print("FOLLOWING")
	# print("==================")
	# print("==================")
	# print("user_obj.follower.all(): ",user_obj.follower.all())
	# print("user_obj.following.all(): ",user_obj.following.all())
	# print("user_obj.following.all().filter: ", filter_follow)

	print("==================")
	print("==================")
	print("following count: ", f1)
	print("followers count: ", f2)

	f1 = Follow.objects.filter(follower=user_obj).values_list('follower', flat=True)
	f2 = Follow.objects.filter(following=user_obj).values_list('following', flat=True)
	
	context = {
		'user': user_obj,
		'events': user_events,
		'followers': f1,
		'following': f2,
	}

	return  render(request, 'profile.html', context)

def event_detail(request , event_id):
	event_obj = Event.objects.get(id=event_id)
	booking_obj = event_obj.booking.all()
	form = BookingForm()
	

	# ============ POSTING ============  
	if request.method == "POST":
		form = BookingForm(request.POST)
		if event_obj.tickets_left() == 0:
			messages.warning(request, "No tickets left. Plsease Booked another Event")
			return redirect('list-event')
		if form.is_valid():
			booking_obj = form.save(commit=False)
			booking_obj.event = event_obj
			booking_obj.user = request.user
			
			if booking_obj.ticket_num > event_obj.tickets_left():
				messages.warning(request, "the number of tickets exceeded the limit")
				return redirect(event_obj)
 
			# booking_obj.event.save()
			booking_obj.save()
			return redirect('event-detail', event_id)
	# ============ POSTING ============ 

	context = {
		"form":form,
		"event" : event_obj,
		"booking": booking_obj,
	}
	return render(request, 'detail.html', context)

def follow(request, user_id):
	if not(request.user.is_authenticated):
		messages.warning(request, "please login")
		return redirect('login')

	user_following = User.objects.get(id=user_id)
	follow, created = Follow.objects.get_or_create(follower=request.user, following=user_following)

	if created:
		following = True
		print("======follow======")
		print("create follow obj")
	else:
		following = False
		follow.delete()
		print("======unfollow======")
		print("delete a follow obj")

	respose = {
		"following": following,
	}
	return JsonResponse(respose, safe=False)


def event_create(request):
	if request.user.is_anonymous:
		return redirect('login')
	form = EventForm()
	if request.method == "POST":
		form = EventForm(request.POST, request.FILES)
		if form.is_valid():
			event_obj = form.save(commit=False)
			event_obj.organized_by = request.user
			event_obj.save()
			return redirect('home')
	context = {
		"form":form,
	}
	return render(request, 'create.html', context)


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
				if request.user.organizer.all().exists():
					return redirect('dashboard')
				else:
					return redirect('list-event')

				messages.success(request, "Welcome Back! %s" %(request.user.username))
				

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
		event_form = EventForm(request.POST, request.FILES, instance=event)
		if event_form.is_valid():
			event_form.save()
			return redirect('event-detail', event_id)

	context = {
		'form': event_form,
		'event': event
	}

	return  render(request, 'update.html', context)


def profile_update(request):
	user = User.objects.get(id=request.user.id)
	print(user.username)
	print(user.first_name)
	print(user.last_name)
	if request.user.is_anonymous:
		return redirect('login')
	user_form = ProfileForm(instance=user)
	print(user)
	print(user_form)
	if request.method == 'POST':
		user_form = ProfileForm(request.POST, request.FILES, instance=user)
		print(user_form.is_valid())
		if user_form.is_valid():
			user1 = user_form.save(commit=False)
			user1.set_password(user.password)
			user1.save()
			return redirect('home')

	context = {
		'user': user,
		'form': user_form,
	}

	return  render(request, 'profile_update.html', context)


def cancelBooking(request, event_id):
	event_obj = Event.objects.get(id=event_id)
	booking_obj = request.user.booking.get(event_id=event_id) 
	today_datetime = datetime.today()

	# current time + 3 hrs
	time_cond = datetime.combine(today_datetime, today_datetime.time()) + timedelta(hours=3)
	eve_datetime = datetime.combine(event_obj.date, event_obj.time) 
	# if event_obj.date == today.date() and time_cond < event_obj.time:
	if  time_cond < eve_datetime:
		messages.success(request, "{} has been canceled".format(event_obj.title))
		booking_obj.delete()
		return redirect('dashboard')
	
	msg = """
	can't be canceled, you can only cancel an event 3 hrs before
	its opening...
	"""
	messages.warning(request, "{} {}".format(event_obj.title, msg))
	return redirect('dashboard')

