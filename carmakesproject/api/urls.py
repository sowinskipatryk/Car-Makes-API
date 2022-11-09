from django.urls import path
from . import views

urlpatterns = [
    path('cars/', views.get_post_cars),
    path('cars/<int:pk>', views.delete_car),
    path('rate/', views.add_rate),
    path('popular/', views.get_popular),
]