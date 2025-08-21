from django.db import models


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


from cargo.models import Cargo
from transport.models import Transport


class Event(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='event_cargo')
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='event_transport')
    event_date = models.DateField(auto_now_add=True)
    arrived = models.BooleanField(default=False)
    act_file = models.FileField(upload_to='documents/acts/', blank=True, null=True)
    invoice_file = models.FileField(upload_to='documents/invoices/', blank=True, null=True)


class Frozen(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='frozen_set')
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, related_name='frozen_set')
    frozen_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата - Час створення")

    def __str__(self):
        return f"Frozen cargo {self.cargo.id} with transport {self.transport.id}"



