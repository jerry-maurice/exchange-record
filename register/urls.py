from django.urls import path, include
from register import views



urlpatterns = [
    path('list/', views.registerList, name='list-register' ),
    path('account/list/', views.registerAdminList, name='account-list-register' ),
    path('account/assigned/', views.registerEmpAssigned, name='emp-assigned-register' ),
]