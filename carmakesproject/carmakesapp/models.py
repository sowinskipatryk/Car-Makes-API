from django.db import models

# Create your models here.

class Car(models.Model):
    make = models.CharField(max_length=256)
    model = models.CharField(max_length=256)
    avg_rating = models.DecimalField(decimal_places=1, max_digits=2)
    rates_number = models.IntegerField(default=0)

    def update_rating(self, id):
        rates = Rate.objects.filter(car_id=id)
        num = 0
        sum = 0
        for rate in rates:
            num += 1
            sum += rate.rating
        self.rates_number = num
        self.avg_rating = sum / num
        print(sum)
        print(num)
        print(self.avg_rating)
        self.save()

    def __str__(self):
        return f"{self.make} {self.model}"


class Rate(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.car_id.make} {self.car_id.model} [{self.rating}]"