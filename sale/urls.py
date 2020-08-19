from django.urls import path, include
from sale import views



urlpatterns = [
    path('app/search-client', views.search_client, name='app-search-client' ),
    path('app/order/<int:order_id>', views.order_detail, name='app-order' ),
    path('app/order/<int:order_id>/payment/<int:detail_id>', views.submit_order, name='app-payment' ),
    path('app/summary/', views.sale_summary, name='sale-summary' ),
    path('account/summary/', views.sales_admin_transfer, name='sales_admin_transfer' ),
    path('account/fee/', views.rate_admin, name='rate_admin' ),
    path('account/sale/<int:order_id>/delete/', views.delete_started_sales, name='delete_started_sales' ),
]
