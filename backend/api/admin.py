from django.contrib import admin
from .models import City, Station, Route, Ticket, Profile

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ('name', 'region')

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address')
    list_filter = ('city',)
    search_fields = ('name', 'city__name', 'address')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('departure_station', 'arrival_station', 'departure_time', 
                   'arrival_time', 'price', 'available_seats', 'carrier')
    list_filter = ('departure_station__city', 'arrival_station__city', 'carrier')
    search_fields = ('departure_station__name', 'arrival_station__name', 'carrier')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'user', 'seat_number', 'purchase_date', 'status')
    list_filter = ('status', 'purchase_date')
    search_fields = ('user__username', 'route__departure_station__name', 
                    'route__arrival_station__name')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'phone', 'birth_date', 'balance')
    search_fields = ('user__username', 'user__email', 'department', 'phone')
