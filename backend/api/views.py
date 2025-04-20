from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from datetime import datetime
from .models import City, Station, Route, Ticket
from .serializers import (
    CitySerializer, StationSerializer, RouteSerializer,
    TicketSerializer, UserSerializer
)

# Create your views here.

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response([])
            
        cities = City.objects.filter(
            Q(name__icontains=query) | 
            Q(region__icontains=query)
        )
        serializer = self.get_serializer(cities, many=True)
        return Response(serializer.data)

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def by_city(self, request):
        city_id = request.query_params.get('city_id')
        if city_id:
            stations = Station.objects.filter(city_id=city_id)
            serializer = self.get_serializer(stations, many=True)
            return Response(serializer.data)
        return Response({"error": "city_id is required"}, status=status.HTTP_400_BAD_REQUEST)

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        departure_city = request.query_params.get('departure_city', '').strip()
        arrival_city = request.query_params.get('arrival_city', '').strip()
        date = request.query_params.get('date')
        
        if not all([departure_city, arrival_city, date]):
            return Response(
                {"error": "departure_city, arrival_city and date are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ищем маршруты с учетом возможных вариантов написания городов
        routes = Route.objects.filter(
            Q(departure_station__city__name__iexact=departure_city) |
            Q(departure_station__city__name__icontains=departure_city),
            Q(arrival_station__city__name__iexact=arrival_city) |
            Q(arrival_station__city__name__icontains=arrival_city)
        ).filter(departure_time__date=date_obj)
        
        serializer = self.get_serializer(routes, many=True)
        return Response(serializer.data)

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        route = serializer.validated_data['route']
        if route.available_seats > 0:
            route.available_seats -= 1
            route.save()
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("No available seats")
