from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('book/<int:vehicle_id>/', views.book_vehicle, name='book_vehicle'),
]
