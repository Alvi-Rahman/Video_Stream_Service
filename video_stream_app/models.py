from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class SubscriptionType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(
        max_length=50, blank=False, null=False, unique=True)

    def __str__(self) -> str:
        return self.type_name


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    
    subscription_type = models.ForeignKey(SubscriptionType,
                                        on_delete=models.SET_NULL, blank=True, null=True)

    subscription_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    subscription_validity = models.IntegerField(
        default=0, verbose_name='subscription_validity (Months)')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.subscription_type.type_name


class User(AbstractUser):
    TYPE_CHOICES = [
        ('AD', 'Admin'), ('CU', 'Customer')
    ]
    id = models.AutoField(primary_key=True)
    username = models.CharField(
        max_length=255, blank=False, null=False, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, blank=False, null=False)
    phone = models.CharField(max_length=15, null=True, blank=True)
    user_subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL,
                                          blank=True, null=True, related_name="subscription")
    user_type = models.CharField(
        choices=TYPE_CHOICES, max_length=50, blank=True, default="CU")
    is_subscribed = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    purchase_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    __prev_subscription = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__prev_subscription = self.user_subscription

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.__prev_subscription != self.user_subscription:
            self.purchase_date = timezone.now()

        if self.user_subscription and not self.is_subscribed :
            self.is_subscribed = True

        super(User, self).save(*args, **kwargs)


class VideoContent(models.Model):
    id = models.AutoField(primary_key=True)
    content_name = models.CharField(max_length=255, blank=True, null=True)
    content_description = models.TextField(max_length=2000, blank=True, null=True)
    file = models.FileField(upload_to='videos/', null=True, blank=True, verbose_name="content_file")
    allowed_subscription = models.ManyToManyField(SubscriptionType, null=True,
                                                  related_name="subscription_type")

    def __str__(self):
        return self.content_name
