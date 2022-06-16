from django.db import models

# Create your models here.


class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=10)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.hall


class Guest(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='reservation')
    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, related_name='reservation')

    def __str__(self):
        return self.movie.movie
