from django.urls import path, include
from support import views



urlpatterns = [
    path('page/', views.support_page, name='support-page' ),
]