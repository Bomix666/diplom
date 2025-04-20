from rest_framework import serializers
from .models import City, Station, Route, Ticket
from django.contrib.auth.models import User

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'region']

class StationSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    
    class Meta:
        model = Station
        fields = ['id', 'name', 'city', 'city_name', 'address']

class RouteSerializer(serializers.ModelSerializer):
    departure_city = serializers.CharField(source='departure_station.city.name', read_only=True)
    arrival_city = serializers.CharField(source='arrival_station.city.name', read_only=True)
    departure_station_name = serializers.CharField(source='departure_station.name', read_only=True)
    arrival_station_name = serializers.CharField(source='arrival_station.name', read_only=True)
    
    class Meta:
        model = Route
        fields = [
            'id', 'departure_station', 'arrival_station',
            'departure_city', 'arrival_city',
            'departure_station_name', 'arrival_station_name',
            'departure_time', 'arrival_time',
            'price', 'total_seats', 'available_seats',
            'carrier', 'bus_model', 'service_class'
        ]

class TicketSerializer(serializers.ModelSerializer):
    route_info = RouteSerializer(source='route', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'route', 'route_info', 'user', 'user_email', 'seat_number', 'purchase_date', 'status']
        read_only_fields = ['purchase_date']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}} 