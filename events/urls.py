from django.urls import path
from .views import (
	Login,
	Logout,
	Signup,
	home,
	event_detail,
	update_event,
	event_create,
	dashboard_event,
    booking_event,
    list_event,
)

urlpatterns = [
    path('', home, name='home'),
 
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('detail/<int:event_id>/', event_detail, name='event-detail'),
    path('create/', event_create, name='event-create'),
    path('<int:event_id>/update/', update_event, name='event-update'),

    path('<int:event_id>/booking/', booking_event, name='booking-event'),
    
    path('dashboard/', dashboard_event, name='dashboard'),
    
    # a list page that'll list all upcoming events 
    path('list/', list_event, name='list-event'),


]