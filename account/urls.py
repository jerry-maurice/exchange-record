from django.urls import path, include
from account import views



urlpatterns = [
    path('dashboard/', views.account_dashboard, name='account-dashboard' ),
    path('profile/', views.account_profile, name='account-profile' ),
    path('account-profile-password/', views.account_profile_password, name='account-profile-password' ),
    path('account-rates/', views.rate_setup, name='account-rates' ),
    path('delete-rates/<int:rate_id>', views.rate_delete, name='delete-rates' ),
    path('employees/', views.account_employees, name='account-employees' ),
    path('clients/', views.account_clients, name='account-clients' ),
    path('employees/<int:employee_id>/transactions/', views.account_emp_transfer, name='account-employee-transfer' ),
    path('transactions/<int:detail_id>/', views.account_transfer, name='account-transfer' ),
] 