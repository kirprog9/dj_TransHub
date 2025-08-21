from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from main.models import Country,City, Region
import math
from django.utils.timezone import now


class Transport(models.Model):

    class Status(models.IntegerChoices):
        UNABLE = 0, 'Недоступний'
        ABLE = 1, 'Доступний'

    STATUS_CHOICES = [
        ('Search', 'Searching'),
        ('IN_TRANSIT', 'In Transit'),
        ('Busy', 'Busy'),
    ]

    loading_date = models.DateField()
    country_from = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='country_from_tr',
                                     verbose_name="Країна віправлення")
    region_from = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='region_from_tr',
                                    verbose_name="Регіон віправлення")
    city_from = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='city_from_tr',
                                  verbose_name="Місто віправлення")

    country_to = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='country_to_tr',
                                   verbose_name="Країна призанчення")
    region_to = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='region_to_tr',
                                  verbose_name="Регіон призанчення")
    city_to = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='city_to_tr',
                                verbose_name="Місто призанчення")

    brand = models.CharField(max_length=100, verbose_name="Бренд")
    model = models.CharField(max_length=100, verbose_name="Модель")
    license_plate = models.CharField(max_length=8, unique=True, verbose_name="Номерний знак")
    year = models.PositiveIntegerField(verbose_name="Рік випуску",validators=[MinValueValidator(1950), MaxValueValidator(2024)])
    max_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Максимальна вага (кг)",)
    max_volume = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Максимальний об'єм (м³)")

    body_type = models.ManyToManyField('BodyType', verbose_name="Тип кузова", related_name='body_type')
    load_unload = models.ManyToManyField('LoadUnload',verbose_name="Завантаження/Розвантаження", related_name='load_unload')
    permissions = models.ManyToManyField('Permissions',verbose_name="Дозволи", related_name='permissions')

    photo = models.ImageField(upload_to='transport_photos/%Y/%m/%d/', blank=True, verbose_name="Фото")
    notes = models.TextField(blank=True, verbose_name="Примітки")
    published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.ABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    freeze = models.BooleanField(default=False, verbose_name="Заморожування")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Search', verbose_name="Статус")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, default=None, related_name='author1')

    class Meta:
        verbose_name = "Транпорт"
        verbose_name_plural = "Транпорт"

    def get_absolute_url(self):
        return reverse('transport:detail', kwargs={"tr_pk": self.pk})

    def get_distance(self):
        R = 6371.0
        city1 = City.objects.get(id=self.city_from.id)
        city2 = City.objects.get(id=self.city_to.id)
        if city1 == city2:
            return 10
        lat1 = city1.latitude
        lon1 = city1.longitude
        lat2 = city2.latitude
        lon2 = city2.longitude

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1


        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return round(distance,2)

    def get_time(self):
        delta = now() - self.updated_at
        seconds = delta.total_seconds()

        if seconds < 60:
            return f"{int(seconds)} секунд тому"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{int(minutes)} хвилин тому"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{int(hours)} годин тому"
        else:
            days = seconds // 86400
            return f"{int(days)} днів тому"

class LoadUnload(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Permissions(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BodyType(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
