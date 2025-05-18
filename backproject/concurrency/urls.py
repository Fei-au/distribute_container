from django.urls import path
from . import views

urlpatterns = [
    # Add your order-specific URL patterns here, for example:
    # path('create/', views.create_order, name='create_order'),
    # path('list/', views.order_list, name='order_list'),
    path('', views.index, name='index'),
    path('testio/', views.testio, name='testio'),
    path('testcpu/', views.testcpu, name='testcpu'),
    path('testasyncio/', views.testasyncio, name='testasyncio'),
    path('testasynccpu/', views.testasynccpu, name='testasynccpu'),
]
