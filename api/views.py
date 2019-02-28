from rest_framework.generics import (
	ListAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	DestroyAPIView,
	CreateAPIView,
)

from events.models import Event, Booking
from django.contrib.auth.models import User


from .serializers import (
	EventListSerializer,
	EventUpdateCreateSerializer,
	RegistrationSerializer,
	EventDetailSerializer,
	EventBookingListSerializer,
	EventBookSerializer,
	EventUsersBookingListSerializers,
	BookedEventSerializer,
)

import datetime
from rest_framework.permissions import IsAuthenticated
from .permissions import IsEventOrg

class EventList(ListAPIView):
	today = datetime.datetime.today().date()
	queryset = Event.objects.filter(date__gte = today)
	serializer_class = EventListSerializer
	permission_classes = [IsAuthenticated,]


class EventDetail(RetrieveAPIView):
	today = datetime.datetime.today().date()
	queryset = Event.objects.filter(date__gte = today)
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	serializer_class = EventDetailSerializer
	permission_classes = [IsAuthenticated,]


class EventOrganizerList(ListAPIView):
	serializer_class = EventListSerializer
	permission_classes = [IsAuthenticated,]
	def get_queryset(self):
		user = self.request.user
		return user.organizer.all()


class EventBookingList(ListAPIView):
	serializer_class = EventBookingListSerializer
	permission_classes = [IsAuthenticated,]
	def get_queryset(self):
		user = self.request.user
		return user.booking.all()


class EventUsersBookingList(RetrieveAPIView):
	queryset = Event.objects.all()
	serializer_class = EventUsersBookingListSerializers
	permission_classes = [IsAuthenticated,]
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'


class EventCreate(CreateAPIView):
	serializer_class = EventListSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(organized_by=self.request.user)


class EventUpdate(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = EventUpdateCreateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsEventOrg,]	


class BookEvent(CreateAPIView):
	serializer_class = BookedEventSerializer
	permission_classes = [IsAuthenticated,]

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)



class RegisterView(CreateAPIView):
	serializer_class = RegistrationSerializer