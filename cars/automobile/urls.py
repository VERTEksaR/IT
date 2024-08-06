from django.urls import path

from automobile.views import (
    Cars,
    CarItem
)

app_name = "automobiles"

urlpatterns = [
    path('cars/', Cars.as_view()),
    path('cars/<int:car_pk>/', CarItem.as_view()),
]
