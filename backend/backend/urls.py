"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import HomePageView, TicketsPageView, RoutesPageView, AboutPageView, ProfilePageView
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from api.forms import CustomUserCreationForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('tickets/', TicketsPageView.as_view(), name='tickets'),
    path('routes/', RoutesPageView.as_view(), name='routes'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='api/login.html'), name='login'),
    path('accounts/register/', CreateView.as_view(
        template_name='api/registration.html',
        form_class=CustomUserCreationForm,
        success_url='/accounts/login/'
    ), name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
