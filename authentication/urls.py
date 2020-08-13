from django.urls import path, include
from authentication import views



urlpatterns = [
    path('login/', views.authentication, name='login-view' ),
    path('logout/', views.loging_out, name='logout-view' ),
    path('locked/', views.locked, name='locked-view' ),
]