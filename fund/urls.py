from django.urls import path, include
from fund import views



urlpatterns = [
    path('overview/', views.fund_overview, name='fund-overview' ),
    path('<int:fund_id>/deposit/', views.fund_deposit, name='fund-deposit' ),
    path('<int:fund_id>/log/', views.log_display, name='fund-log' ),
    path('<int:fund_id>/delete/', views.delete_fund, name='fund-delete' ),
]