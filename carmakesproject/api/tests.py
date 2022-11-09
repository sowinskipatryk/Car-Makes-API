from rest_framework.test import APITestCase
from rest_framework import status
from carmakesapp.models import Car


class CarMakesTests(APITestCase):
    def test_get_cars(self):
        url = 'cars/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_car(self):
        url = 'cars/'
        data = {'Make': 'Opel', 'Model': 'Astra'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Car.objects.filter(make="Opel").exists())
        self.assertTrue(Car.objects.filter(make="Astra").exists())

    def test_delete_car(self):
        url = 'cars/4'
        car = Car.objects.get(id=4)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Car.objects.filter(make=car.make).exists())
        self.assertFalse(Car.objects.filter(make=car.model).exists())

    def test_get_popular(self):
        url = 'popular/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)