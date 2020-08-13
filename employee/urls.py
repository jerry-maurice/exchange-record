from django.urls import path, include
from employee import views



urlpatterns = [
    path('dashboard/', views.dashboard, name='emp-dashboard' ),
    path('profile/', views.profile, name='emp-profile' ),
    path('profile-password/', views.profile_password, name='emp-password'),
    path('schedule/', views.schedule, name='emp-schedule')
]