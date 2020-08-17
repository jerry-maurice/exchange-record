from django.urls import path, include
from register import views



urlpatterns = [
    path('list/', views.registerList, name='list-register' ),
    path('account/list/', views.registerAdminList, name='account-list-register' ),
    path('account/assigned/', views.registerEmpAssigned, name='emp-assigned-register' ),
    path('employee/<int:emp_id>/assigned/', views.assign_register, name='assigned-register' ),
    path('employee/<int:emp_id>/register/<int:register_id>/', views.remove_assign_register, name='remove_assign_register' ),
]