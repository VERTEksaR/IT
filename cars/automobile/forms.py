import datetime

from django import forms

from .models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["brand", "model", "year", "fuel_type", "transmission",
                  "mileage", "price"]

    def clean(self):
        super(CarForm, self).clean()

        year = self.cleaned_data.get('year')
        mileage = self.cleaned_data.get('mileage')
        price = self.cleaned_data.get('price')

        now_year = datetime.datetime.now().year

        if year < 1940:
            self._errors['year'] = self.error_class([
                'Минимальный год выпуска: 1940'
            ])
        elif year > now_year:
            self._errors['year'] = self.error_class([
                'Выпуск автомобиля не должен быть в будущем'
            ])

        if mileage < 0:
            self._errors['mileage'] = self.error_class([
                'Пробег не может быть отрицательным'
            ])

        if price < 0:
            self._errors['price'] = self.error_class([
                'Цена не может быть отрицательной'
            ])

        return self.cleaned_data
