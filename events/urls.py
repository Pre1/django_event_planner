from django.urls import path
from .views import Login, Logout, Signup, home, event_detail

urlpatterns = [
	path('', home, name='home'),
 
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('detail/<int:event_id>/', event_detail, name='event-detail'),
]