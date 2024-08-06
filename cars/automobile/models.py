from django.db import models


TYPE_OF_FUEL = {
    "Бензин": "Бензин",
    "Дизель": "Дизель",
    "Электричество": "Электричество",
    "Гибрид": "Гибрид"
}

TYPE_OF_KPP = {
    "Механическая": "Механическая",
    "Автоматическая": "Автоматическая",
    "Вариатор": "Вариатор",
    "Робот": "Робот"
}


class Car(models.Model):
    """Модель автомобиля"""
    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    brand = models.CharField(max_length=127, null=False, blank=False, verbose_name='Марка')
    model = models.CharField(max_length=127, null=False, blank=False, verbose_name='Модель')
    year = models.IntegerField(null=False, blank=False, verbose_name='Год выпуска')
    fuel_type = models.CharField(max_length=15, null=False, blank=False, choices=TYPE_OF_FUEL, verbose_name='Тип топлива')
    transmission = models.CharField(max_length=15, null=False, blank=False, choices=TYPE_OF_KPP, verbose_name='Тип КПП')
    mileage = models.IntegerField(null=False, blank=False, verbose_name='Пробег')
    price = models.IntegerField(null=False, blank=False, verbose_name='Цена')

    def __str__(self):
        return f'{self.brand} | {self.model}'
