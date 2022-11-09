from rest_framework.test import APITestCase
from rest_framework import status
from .models import Car, Rate
import random

# Create your tests here.

make = ['Toyota', 'Mazda', 'Chrysler', 'Audi', 'Honda', 'Subaru', 'Porsche']
model = ['Prius', 'MX-5', '300', 'A6', 'Accord', 'Impreza', 'Taycan']


def populate_db():
    for i in range(7):
        Car.objects.get_or_create(make=make[i], model=model[i])


class CarMakesTestCase(APITestCase):
    def test_post_car(self):
        i = random.randint(1, 7)
        data = {"make": make[i], "model": model[i]}
        response = self.client.post('/cars/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Car.objects.filter(make=make[i]).exists())
        self.assertTrue(Car.objects.filter(model=model[i]).exists())

    def test_get_cars(self):
        url = '/cars/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_car(self):
        populate_db()
        url = '/cars/4'
        car = Car.objects.get(id=4)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Car.objects.filter(make=car.make).exists())
        self.assertFalse(Car.objects.filter(make=car.model).exists())

    def test_get_popular(self):
        url = '/popular/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rate(self):
        populate_db()
        data = {"car_id": 3, "rating": 4}
        response = self.client.post('/rate/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Rate.objects.get(id=1).car_id, 3)
        self.assertEqual(Rate.objects.get(id=1).rating, 4)
