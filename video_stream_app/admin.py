from django.contrib import admin
from .models import Subscription, User, SubscriptionType, VideoContent


# Register your models here.


class SubscriptionAdmin(admin.ModelAdmin):
    model = Subscription
    list_display = [
        "subscription_type",
        "subscription_price",
        "subscription_validity"
    ]

    search_fields = [
        "subscription_type__type_name",
        "subscription_price"
    ]



class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = [
        "username",
        "email",
        "is_superuser",
        "user_type"
    ]

    search_fields = [
        "username",
        "full_name",
        "email",
        "phone",
    ]

    list_filter = [
        "is_subscribed",
        "is_blocked"
    ]


class SubscriptionTypeAdmin(admin.ModelAdmin):
    model = SubscriptionType
    list_display = [
        "type_name"
    ]

    search_fields = [
        "type_name"
    ]


class VideoContentAdmin(admin.ModelAdmin):
    model = VideoContent
    list_display = [
        "content_name",
        "content_description",
        "file",
    ]


admin.site.register(VideoContent, VideoContentAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(SubscriptionType, SubscriptionTypeAdmin)
