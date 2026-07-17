from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('<int:pk>/', views.OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('<int:pk>/export/excel/', views.export_excel, name='order-export-excel'),
    path('<int:pk>/export/pdf/', views.export_pdf, name='order-export-pdf'),
    path('<int:pk>/view/', views.order_detail_public, name='order-detail-public'),
]
