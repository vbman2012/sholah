from rest_framework import serializers
from .models import Movie, Guest, Reservation


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'hall', 'movie', 'date', 'reservation')


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('id', 'movie', 'guest')


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'name', 'mobile', 'reservation')
