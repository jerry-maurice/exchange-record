from django.urls import path, include
from sale import views



urlpatterns = [
    path('app/search-client', views.search_client, name='app-search-client' ),
    path('app/order/<int:order_id>', views.order_detail, name='app-order' ),
    path('app/order/<int:order_id>/payment/<int:detail_id>', views.submit_order, name='app-payment' ),
    path('app/sale/summary/', views.sale_summary, name='sale-summary' ),
]