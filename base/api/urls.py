from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_routes),
    path('rooms/', views.get_rooms),
    path('room/<str:pk>/', views.get_room)
]
