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

    path('api/', EventList.as_view(), name = 'api-list'),
    path('api/login/', obtain_jwt_token, name = 'api-login'),
    path('api/create/', EventCreate.as_view(), name = 'api-create'),
    path('api/update/<int:event_id>/', EventUpdate.as_view(), name = 'api-update'),
    path('api/detail/<int:event_id>/', EventDetail.as_view(), name = 'api-events-detail'),
    path('api/org_events/', EventOrganizerList.as_view(), name = 'api-events-org'),
    path('api/booked_events/', EventBookingList.as_view(), name = 'api-events-booking'),
    path('api/book/<int:event_id>/', BookEvent.as_view(), name = 'api-book'),
    path('api/users_booking/<int:event_id>', EventUsersBookingList.as_view(), name = 'users-book'),
]