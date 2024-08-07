from typing import Dict

from drf_yasg.utils import swagger_auto_schema

from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from automobile.models import Car
from automobile.serializers import CarSerializer
from automobile.paginations import CustomPagination, PaginationHandlerMixin


class Cars(APIView, PaginationHandlerMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_summary='Получение списка автомобилей',
        responses={200: CarSerializer(many=True), 204: 'Пустая страница при пагинации и фильтрации', 400: 'Неверные параметры фильтрации'}
    )
    def get(self, request: Request) -> Response:
        if request.query_params:
            try:
                filter_dict = self.filtering(request)
                filtered_cars = Car.objects.filter(**filter_dict).all()
                result_page = self.paginate_queryset(filtered_cars)
                serializer = CarSerializer(result_page, many=True)
            except Exception as exc:
                if str(exc) == 'Invalid page.':
                    return Response({'message': 'Данные на данной странице отсутствуют. Уберите из URI'
                                                '"page" или приравняйте его к 1'}, status=status.HTTP_204_NO_CONTENT)
                return Response({'message': 'Введены некорректные параметры фильтрации'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            cars = Car.objects.all()
            result_page = self.paginate_queryset(cars)
            serializer = CarSerializer(result_page, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Добавление новой записи о машине в БД',
        responses={201: CarSerializer, 400: 'Ошибка при валидации данных'},
        query_serializer=CarSerializer,
        request_body=CarSerializer,
    )
    def post(self, request: Request) -> Response:
        serializer = CarSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def filtering(self, request: Request) -> Dict:
        filtering_fields = dict()

        for key, value in request.query_params.items():
            if key not in ['page_size', 'page']:
                if key in ['mileage_min', 'price_min']:
                    filtering_fields[key[:-4] + '__gte'] = value
                elif key in ['mileage_max', 'price_max']:
                    filtering_fields[key[:-4] + '__lte'] = value
                else:
                    filtering_fields[key] = value

        return filtering_fields


class CarItem(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Получение данных о конкретном автомобиле',
        responses={200: CarSerializer, 404: 'Объект с таким id отсутствует'}
    )
    def get(self, request: Request, car_pk) -> Response:
        try:
            car = Car.objects.get(id=car_pk)
        except Car.DoesNotExist:
            return Response({'message': 'Объект с таким id отсутствует'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CarSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Изменение данных автомобиля',
        responses={201: CarSerializer, 400: 'Ошибка при валидации данных'},
        query_serializer=CarSerializer,
        request_body=CarSerializer
    )
    def patch(self, request: Request, car_pk) -> Response:
        instance = Car.objects.get(id=car_pk)
        serializer = CarSerializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Удаление данных автомобиля',
        responses={200: 'Удалено'}
    )
    def delete(self, request: Request, car_pk) -> Response:
        car = Car.objects.get(id=car_pk)
        car.delete()
        return Response({'message': 'Автомобиль успешно удален из БД'}, status=status.HTTP_200_OK)
