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
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from .forms import UserForm, ProfileForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import logout

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
        context['tickets'] = Ticket.objects.filter(user=self.request.user).exclude(status='cancelled')
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
            'profile': profile,
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
            'profile': profile,
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
            serializer.save(user=self.request.user, status='reserved')
        else:
            raise serializers.ValidationError("No available seats")

class BookingWizardView(LoginRequiredMixin, View):
    template_name = 'api/booking_step.html'

    def get(self, request):
        step = request.GET.get('step', '1')
        context = {'step': step, 'title': 'Бронирование билета'}
        # step 1: выбор типа билета и места
        if step == '1':
            route_id = request.GET.get('route_id')
            context['route_id'] = route_id
            # Здесь можно добавить выбор мест и типа билета
        # step 2: ввод данных пассажира
        elif step == '2':
            pass
        # step 3: подтверждение
        elif step == '3':
            pass
        return render(request, self.template_name, context)

    def post(self, request):
        step = request.POST.get('step', '1')
        # step 1: сохранить выбор типа билета и места
        if step == '1':
            request.session['booking'] = {
                'route_id': request.POST.get('route_id'),
                'ticket_type': request.POST.get('ticket_type'),
                'seat_number': request.POST.get('seat_number'),
            }
            return redirect(f"{reverse('booking')}?step=2")
        # step 2: сохранить данные пассажира
        elif step == '2':
            booking = request.session.get('booking', {})
            booking['passenger_name'] = request.POST.get('passenger_name')
            booking['passenger_birth'] = request.POST.get('passenger_birth')
            booking['is_discount'] = request.POST.get('is_discount')
            request.session['booking'] = booking
            return redirect(f"{reverse('booking')}?step=3")
        # step 3: финальное подтверждение и создание билета
        elif step == '3':
            booking = request.session.get('booking', {})
            from .models import Route, Ticket
            route = Route.objects.get(id=booking['route_id'])
            if route.available_seats > 0:
                route.available_seats -= 1
                route.save()
                Ticket.objects.create(
                    route=route,
                    user=request.user,
                    seat_number=booking['seat_number'],
                    status='reserved'
                )
                del request.session['booking']
                return redirect('tickets')
            else:
                messages.error(request, 'Нет доступных мест на выбранный маршрут.')
                return redirect('routes')
        return redirect('routes')

class CancelTicketView(LoginRequiredMixin, View):
    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id, user=request.user)
            if ticket.status != 'cancelled':
                ticket.status = 'cancelled'
                ticket.save()
                ticket.route.available_seats += 1
                ticket.route.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Уже отменён'}, status=400)
        except Ticket.DoesNotExist:
            return HttpResponseForbidden()

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('register')

class RouteDetailView(DetailView):
    model = Route
    template_name = 'api/route_detail.html'
    context_object_name = 'route'
