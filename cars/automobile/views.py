from django.shortcuts import HttpResponse, render, redirect
from django.views.generic import CreateView
from django.views import View

from automobile.models import Car
from automobile.forms import CarForm


class CarsForm(View):
    def get(self, request, *args, **kwargs):
        form = CarForm(None)
        return render(request, 'cars/cars_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        car = CarForm(request.POST)

        if car.is_valid():
            car.save()

            return HttpResponse('Автомобиль успешно добавлен в базу данных')
        else:
            return render(request, 'cars/cars_create.html', {'form': car})


class CarsList(View):
    def get(self, request, *args, **kwargs):
        print(request)
        return render(request, 'cars/main_list.html')
