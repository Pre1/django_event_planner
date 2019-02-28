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
    list_event,
    profile,
    follow,
    profile_update,
    cancelBooking,
)

urlpatterns = [
    path('', home, name='home'),
 
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('detail/<int:event_id>/', event_detail, name='event-detail'),
    path('create/', event_create, name='event-create'),
    path('<int:event_id>/update/', update_event, name='event-update'),
    
    path('dashboard/', dashboard_event, name='dashboard'),
    path('dashboard/cancel_booking/<int:event_id>/', cancelBooking, name='event-cancel'),
    
    path('list/', list_event, name='list-event'),
    path('profile/update', profile_update, name='profile-update'),
    path('profile/', profile, name='profile'),
    path('follow/<int:user_id>/', follow, name='follow'),


]