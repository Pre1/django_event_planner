from django.urls import path
from .views import (
    EventList,
    EventCreate,
	EventUpdate,
	EventOrganizerList,
	EventDetail,
	EventBookingList,
	BookEvent,
	EventUsersBookingList,
)
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [

	path('api/', EventList.as_view(), name = 'list'),
	path('api/login/', obtain_jwt_token, name = 'login'),
	path('api/create/', EventCreate.as_view(), name = 'create'),
	path('api/update/<int:event_id>/', EventUpdate.as_view(), name = 'update'),
	path('api/detail/<int:event_id>/', EventDetail.as_view(), name = 'events-detail'),
	path('api/org_events/', EventOrganizerList.as_view(), name = 'events-org'),
	path('api/booked_events/', EventBookingList.as_view(), name = 'events-booking'),
	path('api/book/<int:event_id>/', BookEvent.as_view(), name = 'book'),
	path('api/users_booking/<int:event_id>', EventUsersBookingList.as_view(), name = 'users-book'),
]