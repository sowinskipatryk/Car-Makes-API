from rest_framework.response import Response
from rest_framework.decorators import api_view
from carmakesapp.models import Car, Rate
from .serializers import CarSerializer, RateSerializer, PopularSerializer
from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET', 'POST'])
def get_post_cars(request):
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response('Wrong data format! Car should have the make and model.', status=400)
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_rate(request):
    serializer = RateSerializer(data=request.data)
    if not request.data['rating'] in range(1,6):
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