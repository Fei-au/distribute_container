from django.urls import path
from . import views

urlpatterns = [
    path('sub_push/', views.sub_push, name='sub_push'),
]
