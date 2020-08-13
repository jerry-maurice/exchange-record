from django.urls import path
from overview import views


urlpatterns = [
    path('', views.index, name='home' ),
]