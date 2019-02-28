from rest_framework import serializers
from events.models import Event, Booking
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]

class EventListSerializer(serializers.ModelSerializer):
	detail = serializers.HyperlinkedIdentityField(
			view_name = 'events-detail',
			lookup_field = 'id',
			lookup_url_kwarg = 'event_id',
	)

	class Meta:
		model = Event
		fields = ['id', 'title', 'date', 'detail', ]

class BookedEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		exclude = ['user']

	def validate(self, data):
		print("==================")
		print("BookedEventSerializer==================")
		print("self", self)
		print("data", data)
		return  data

class EventBookSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	class Meta:
		model = Booking
		fields = ['user', 'ticket_num']


class EventDetailSerializer(serializers.ModelSerializer):
	booking = EventBookSerializer(many=True)
	class Meta:
		model = Event
		fields = '__all__'

class EventUpdateCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Event
		exclude = ['organized_by']


class EventBookingListSerializer(serializers.ModelSerializer):
	event = EventListSerializer()
	class Meta:
		model = Booking
		fields = ['id', 'event', 'timestamp', 'ticket_num']


class EventUsersBookingListSerializers(serializers.ModelSerializer):
		
	booked_users = serializers.SerializerMethodField() 
	class Meta:
		model = Event
		fields = ['booked_users']

	def get_booked_users(self, obj):
		users = obj.booking.all()
		return EventBookSerializer(users, many = True).data

class RegistrationSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ['username', 'password']

	def create(self, validated_data):
		my_username = validated_data['username']
		my_password = validated_data['password']

		new_user = User(username=my_username)
		new_user.set_password(my_password)
		new_user.save()

		return validated_data
