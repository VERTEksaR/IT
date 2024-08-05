from django.urls import path

from automobile.views import (
    CarsForm,
    CarsList,
)

app_name = "automobiles"

urlpatterns = [
    path('create/', CarsForm.as_view(), name='index'),
    path('cars/', CarsList.as_view()),
]
