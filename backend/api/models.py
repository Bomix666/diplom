from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}, {self.region}"
    
    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

class Station(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='stations')
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.name}, {self.city.name}"
    
    class Meta:
        verbose_name = "Станция"
        verbose_name_plural = "Станции"

class Route(models.Model):
    departure_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='departures')
    arrival_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='arrivals')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    carrier = models.CharField(max_length=100)
    bus_model = models.CharField(max_length=100)
    service_class = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.departure_station.city.name} - {self.arrival_station.city.name}"
    
    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"

class Ticket(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    seat_number = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='active')
    
    def __str__(self):
        return f"Билет {self.id} на маршрут {self.route}"
    
    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Баланс (₽)")

    def __str__(self):
        return f"Профиль {self.user.username}"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
