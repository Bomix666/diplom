from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from datetime import datetime
from .models import City, Station, Route, Ticket, Profile
from .serializers import (
    CitySerializer, StationSerializer, RouteSerializer,
    TicketSerializer, UserSerializer
)
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from .forms import UserForm, ProfileForm

class HomePageView(TemplateView):
    template_name = 'api/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Система бронирования билетов'
        return context

class TicketsPageView(LoginRequiredMixin, TemplateView):
    template_name = 'api/tickets.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои билеты'
        context['tickets'] = Ticket.objects.filter(user=self.request.user)
        return context

class RoutesPageView(TemplateView):
    template_name = 'api/routes.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Маршруты'
        routes = Route.objects.all()
        departure_city = self.request.GET.get('departure_city')
        arrival_city = self.request.GET.get('arrival_city')
        date = self.request.GET.get('date')
        if departure_city:
            routes = routes.filter(departure_station__city__name__icontains=departure_city)
        if arrival_city:
            routes = routes.filter(arrival_station__city__name__icontains=arrival_city)
        if date:
            routes = routes.filter(departure_time__date=date)
        context['routes'] = routes
        return context

class AboutPageView(TemplateView):
    template_name = 'api/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О нас'
        return context

class ProfilePageView(LoginRequiredMixin, View):
    template_name = 'api/profile.html'

    def get(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            'title': 'Профиль',
        })

    def post(self, request):
        profile, created = Profile.objects.get_or_create(user=request.user)
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Данные успешно обновлены!')
            return redirect('profile')
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
            'title': 'Профиль',
        })

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
