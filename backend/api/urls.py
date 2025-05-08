from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import BookingWizardView, CancelTicketView, CustomLogoutView

router = DefaultRouter()
router.register(r'cities', views.CityViewSet)
router.register(r'stations', views.StationViewSet)
router.register(r'routes', views.RouteViewSet)
router.register(r'tickets', views.TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
    path('booking/', BookingWizardView.as_view(), name='booking'),
    path('tickets/cancel/<int:ticket_id>/', CancelTicketView.as_view(), name='cancel_ticket'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
] 