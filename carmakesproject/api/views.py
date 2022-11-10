from rest_framework.response import Response
from rest_framework.decorators import api_view
from carmakesapp.models import Car, Rate
from .serializers import CarSerializer, RateSerializer, PopularSerializer
from django.core.exceptions import ObjectDoesNotExist
import requests


@api_view(['GET', 'POST'])
def get_post_cars(request):
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            post_make = request.data['make']
            post_model = request.data['model']
            try:
                makes = requests.get('https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json')
                models = requests.get(f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{post_make}?format=json')

                make_found = False
                model_found = False
                for make in makes.json()['Results']:
                    if make['Make_Name'] == post_make.upper():
                        make_found = True
                        break

                for model in models.json()['Results']:
                    if model['Model_Name'] == post_model:
                        model_found = True
                        break

                if make_found and model_found:
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response('The car with given make and model does not exist in the validation database!',
                                    status=400)
            except requests.exceptions.InvalidSchema:
                return Response('Validation database failed!', status=500)
        return Response('Wrong data format! Car should have the make and model.', status=400)
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_rate(request):
    serializer = RateSerializer(data=request.data)
    if not request.data['rating'] in range(1, 6):
        return Response('Rating must be an integer from 1 to 5!', status=400)
    if serializer.is_valid():
        serializer.save()
        id = request.data['car_id']
        car = Car.objects.get(id=id)
        car.update_rating(id)
        return Response(serializer.data)
    return Response('The car with given ID does not exist in the database!', status=400)


@api_view(['DELETE'])
def delete_car(request, pk):
    try:
        car = Car.objects.get(id=pk)
        car.delete()
        return Response('Car deleted successfully!')
    except ObjectDoesNotExist:
        return Response('The car with given ID does not exist in the database!', status=400)


@api_view(['GET'])
def get_popular(request):
    cars = Car.objects.order_by('-rates_number')
    serializer = PopularSerializer(cars, many=True)
    return Response(serializer.data)
