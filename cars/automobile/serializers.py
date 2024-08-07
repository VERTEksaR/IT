import datetime

from rest_framework import serializers

from automobile.models import Car


class CarSerializer(serializers.Serializer):
    """Сериализатор для модели автомобиля"""
    id = serializers.ReadOnlyField()
    brand = serializers.CharField(max_length=127, allow_null=False, allow_blank=False, required=True)
    model = serializers.CharField(max_length=127, allow_null=False, allow_blank=False, required=True)
    year = serializers.IntegerField(allow_null=False, required=True)
    fuel_type = serializers.CharField(max_length=15, allow_null=False, allow_blank=False, required=True)
    transmission = serializers.CharField(max_length=20, allow_null=False, allow_blank=False, required=True)
    mileage = serializers.IntegerField(allow_null=False, required=True)
    price = serializers.IntegerField(allow_null=False, required=True)

    def create(self, validated_data):
        """Метод для создания объекта через сериализатор"""
        return Car.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Метод для обновления отдельных полей объекта через сериализатор"""
        instance.brand = validated_data.get('brand', instance.brand)
        instance.model = validated_data.get('model', instance.model)
        instance.year = validated_data.get('year', instance.year)
        instance.fuel_type = validated_data.get('fuel_type', instance.fuel_type)
        instance.transmission = validated_data.get('transmission', instance.transmission)
        instance.mileage = validated_data.get('mileage', instance.mileage)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

    def validate_year(self, value):
        """Метод для валидации года"""
        now_year = datetime.datetime.now().year

        if value < 1940:
            raise serializers.ValidationError('Минимальный год выпуска: 1940')
        elif value > now_year:
            raise serializers.ValidationError('Выпуск автомобиля не должен быть в будущем')

        return value

    def validate_fuel_type(self, value):
        """Метод для валидации типа топлива"""
        if value not in ['бензин', 'дизель', 'электричество', 'гибрид']:
            raise serializers.ValidationError('Топливом должен быть элемент из списка: бензин, дизель, электричество, гибрид')

        return value

    def validate_transmission(self, value):
        """Метод для валидации типа КПП"""
        if value not in ['механическая', 'автоматическая', 'вариатор', 'робот']:
            raise serializers.ValidationError('КПП должен быть элемент из списка: механическая, автоматическая, вариатор, робот')

        return value

    def validate_mileage(self, value):
        """Метод для валидации пробега"""
        if value < 0:
            raise serializers.ValidationError('Пробег не может быть отрицательным')

        return value

    def validate_price(self, value):
        """Метод для валидации цены"""
        if value < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')

        return value
