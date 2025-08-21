from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
class User(AbstractUser):
    ROLE_CHOICES = [
        ('SHIPPER', 'Відправник вантажу'),
        ('TRANSPORTER', 'Перевізник'),
        ('FORWARD', 'Експедитор'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    about = models.TextField(blank=True, null=True)
    third_name = models.CharField(max_length=100, blank=True, null=True)
    activity_directions = models.ManyToManyField('ActivityDirection', related_name='users')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name="Фото")
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=50)
    tel = models.BigIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(999999999999)], null=True)
    name_company = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.username

    def get_absolute_url2(self):
        return reverse('post', kwargs={"name_slug": self.username})

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.third_name}"

    def update_rating(self, target_user):
        reviews = Review.objects.filter(target_user=target_user)
        complaints = Complaint.objects.filter(target_user=target_user).count()

        if reviews.exists():
            avg_rating = sum([review.rating for review in reviews]) / reviews.count()
            print(avg_rating)
            self.rating = (avg_rating / 5) * 100 - (complaints * 5)
            print(self.rating)
            self.rating = max(0, min(self.rating, 100))  # Обмежити від 0 до 100
        else:
            self.rating = 50.00 - (complaints * 5)  # Початковий рейтинг
        self.save()

class ActivityDirection(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='reviews', on_delete=models.CASCADE)
    target_user = models.ForeignKey(get_user_model(), related_name='rev_target_user',verbose_name="Користувач якому присвячуется Відгук", on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name="Рейтинг")
    comment = models.TextField(verbose_name="Опис")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} от {self.user} до  {self.target_user}: {self.comment}  "

    def get_absolute_url(self):
        return reverse('log_good')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        target_user = self.target_user
        self.target_user.update_rating(target_user)

class Complaint(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='complaints', on_delete=models.CASCADE)
    target_user = models.ForeignKey(get_user_model(), related_name='com_target_user',verbose_name="Користувач якому присвячуется Скарга", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Опис")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Скарга  від {self.user} до {self.target_user} з приводу {self.description}"

    def get_absolute_url(self):
        return reverse('log_good')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        target_user = self.target_user
        self.target_user.update_rating(target_user)
