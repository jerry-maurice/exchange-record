from django.urls import path, include
from country import views



urlpatterns = [
    path('list/', views.countryList, name='country-list' ),
    path('account/add/', views.addCountry, name='country-add' ),
]