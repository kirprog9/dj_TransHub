from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from main.models import Country, City, Region

from django.utils.timezone import now
import math


class Cargo(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубліковано'

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
    ]

    PACKAGING_CHOICES = [
        ('Без упаковки', 'Без упакування'),
        ('EURO 1,2x0,8 м', 'EURO 1,2x0,8 м'),
        ('FIN 1,2x1 м', 'FIN 1,2x1 м'),
        ('1x1 м', '1x1 м'),
        ('1,1x1,1 м', '1,1x1,1 м'),
        ('1,2x1,2 м', '1,2x1,2 м'),
        ('Нестандартна', 'Нестандартна'),
        ('Біг-бег', 'Біг-бег'),
        ('Мішок', 'Мішок'),
        ('В’язка', 'В’язка'),
        ('Сітка', 'Сітка'),
        ('Тюк', 'Тюк'),
        ('Блок', 'Блок'),
        ('Бочка', 'Бочка'),
        ('Чушка', 'Чушка'),
        ('Ящик', 'Ящик'),
        ('Коробка', 'Коробка'),
        ('Пачка', 'Пачка'),
        ('Упаковка', 'Упаковка'),
        ('Swap body', 'Swap body'),
        ("45'", "45'"),
        ("40'", "40'"),
        ("20'", "20'"),
        ('Бухта', 'Бухта'),
        ('Рулон', 'Рулон'),
        ('Барабан', 'Барабан'),
        ('Балон', 'Балон'),
        ('Каністра', 'Каністра'),
        ('Відро', 'Відро'),
        ('Навалом', 'Навалом'),
        ('Насипом', 'Насипом')
    ]

    PAYMENT_TYPE2_CHOICES = [
        ('CASH', 'готівка'),
        ('BANK', 'безготівка'),
        ('COMBO', 'комб.'),
        ('ELEC', 'ел. платіж'),
        ('CARD', 'картка'),
    ]

    PAYMENT_MOMENT_CHOICES = [
        ('LOAD', 'На загрузці'),
        ('UNLOAD', 'На вигрузці'),
        ('ORIGINALS', 'По оригіналам'),
        ('DEFERRED', 'Відсрочка оплати'),
    ]

    title = models.CharField(max_length=100, verbose_name="Назва вантажу")

    country_from = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='country_from_cargos',
                                     verbose_name="Країна віправлення")
    region_from = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='region_from_cargos',
                                    verbose_name="Регіон віправлення")
    city_from = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='city_from_cargos',
                                  verbose_name="Місто віправлення")

    country_to = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='country_to_cargos',
                                   verbose_name="Країна призанчення")
    region_to = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='region_to_cargos',
                                  verbose_name="Регіон призанчення")
    city_to = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='city_to_cargos',
                                verbose_name="Місто призанчення")

    weight_max = models.PositiveIntegerField(verbose_name="Вага до (кг)", validators=[MinValueValidator(1)])
    volume_max = models.PositiveIntegerField(verbose_name="Об'єм до (м³)", null=True, validators=[MinValueValidator(1)])
    length = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Довжина (м)",
                                 validators=[MinValueValidator(0.01), MaxValueValidator(99.99)], null=True)
    width = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Ширина (м)",
                                validators=[MinValueValidator(0.01), MaxValueValidator(99.99)], null=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Висота (м)",
                                 validators=[MinValueValidator(0.01), MaxValueValidator(99.99)], null=True)
    packaging = models.CharField(max_length=100, choices=PACKAGING_CHOICES, verbose_name="Пакування")
    body_type = models.ManyToManyField('BodyType', verbose_name="Тип кузова", related_name='body_type')
    load_unload = models.ManyToManyField('LoadUnload', verbose_name="Завантаження/Розвантаження",
                                         related_name='load_unload')
    permissions = models.ManyToManyField('Permissions', verbose_name="Дозволи", related_name='permissions')
    payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPE2_CHOICES, verbose_name="Форма оплати",
                                    default='default')
    amount = models.PositiveIntegerField(verbose_name="Сума коштів", blank=True, null=True)
    currency = models.CharField(max_length=10, verbose_name="Валюта", default='грн')
    payment_moment = models.CharField(max_length=100, choices=PAYMENT_MOMENT_CHOICES, verbose_name="Момент оплати")
    photo = models.ImageField(upload_to='cargo_photos/%Y/%m/%d/', blank=True, verbose_name="Фото")
    notes = models.TextField(blank=True, verbose_name="Примітка")
    published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                    default=Status.DRAFT, verbose_name="Опубліковано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    freeze = models.BooleanField(default=False, verbose_name="Заморожування")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Статус")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               null=True, default=None, related_name='author')

    class Meta:
        verbose_name = "Вантаж"
        verbose_name_plural = "Вантажи"

    def get_absolute_url(self):
        return reverse('home')

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

    def get_per_km(self):
        a = self.amount / self.get_distance()
        return round(a,2)

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


