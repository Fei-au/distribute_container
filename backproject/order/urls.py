from django.urls import path
from . import views

urlpatterns = [
    # Add your order-specific URL patterns here, for example:
    # path('create/', views.create_order, name='create_order'),
    # path('list/', views.order_list, name='order_list'),
    path('', views.order, name='order'),
    path('add/', views.add_order, name='add_order'),
    path('delete/', views.delete_order, name='delete_order'),
    path('update/', views.update_order, name='update_order'),
    path('list/', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
