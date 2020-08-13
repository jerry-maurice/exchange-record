from django.urls import path, include
from register import views



urlpatterns = [
    path('list/', views.registerList, name='list-register' ),
]