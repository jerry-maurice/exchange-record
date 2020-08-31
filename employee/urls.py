from django.urls import path, include
from employee import views



urlpatterns = [
    path('dashboard/', views.dashboard, name='emp-dashboard' ),
    path('profile/', views.profile, name='emp-profile' ),
    path('profile-password/', views.profile_password, name='emp-password'),
    path('schedule/', views.schedule, name='emp-schedule'),
    path('<int:emp_id>/schedule/', views.add_schedule, name='emp-schedule-add'),
    path('<int:emp_id>/schedule/<int:schedule_id>/delete', views.delete_schedule, name='emp-schedule-delete')
]