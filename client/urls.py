from django.urls import path
from client import views


urlpatterns = [
    path('list/', views.client, name='clients' ),
    path('add/', views.add_client, name='add-client' ),
]