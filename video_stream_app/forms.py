from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from .models import Subscription, SubscriptionType, User, VideoContent, UserPayments
from .widgets import PictureWidget


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=255, help_text='Required. Inform a valid email address.',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    full_name = forms.CharField(max_length=15, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'full_name')
    #
    # def __init__(self, *args, **kwargs):
    #     super(UserRegistrationForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control'


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class SubscriptionForm(forms.ModelForm):
    subscription_type = forms.ModelChoiceField(queryset=SubscriptionType.objects.all(), required=True,
                                               widget=forms.Select(attrs={'class': 'form-control'}))
    subscription_price = forms.DecimalField(max_digits=10, decimal_places=2,
                                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    subscription_validity = forms.IntegerField(required=True,
                                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Subscription
        fields = ('subscription_type', 'subscription_price', 'subscription_validity')


class SubscriptionTypeForm(forms.ModelForm):
    type_name = forms.CharField(max_length=50, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = SubscriptionType
        fields = ('type_name',)


class UserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=255,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(max_length=255, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(max_length=255,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=255, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_subscription = forms.ModelChoiceField(queryset=Subscription.objects.all(),
                                               widget=forms.Select(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(choices=User.TYPE_CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    is_subscribed = forms.BooleanField(required=False)
    is_blocked = forms.BooleanField(required=False)
    purchase_date = forms.DateTimeField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'phone', 'user_subscription',
                  'user_type', 'is_subscribed', 'is_blocked', 'purchase_date')


class VideoContentUploadForm(forms.ModelForm):

    content_name = forms.CharField(max_length=255, required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    content_description = forms.CharField(max_length=255, required=False,
                                          widget=forms.Textarea(attrs={'class': 'form-control'}))
    file_preview = forms.FileField(required=False,
                                   widget=PictureWidget(
                                       id='myvideo', link="", video=True))

    file = forms.FileField(required=True,
                           widget=forms.FileInput(attrs={
                                          'class': 'form-control',
                                          'type': 'file'
                                      }))
    cover_image_preview = forms.ImageField(required=False,
                                           widget=PictureWidget(id='myimage', link=""))
    cover_image = forms.FileField(required=False,
                                  widget=forms.FileInput(
                                      attrs={
                                          'class': 'form-control',
                                          'onchange': 'readURL(this);',
                                          'type': 'file'
                                      }))
    allowed_subscription = forms.ModelMultipleChoiceField(queryset=SubscriptionType.objects.all(),
                                                          widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = VideoContent
        fields = ('content_name', 'content_description', 'file_preview',
                  'file', 'cover_image_preview',
                  'cover_image', 'allowed_subscription'
                  )


class PaymentForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices=UserPayments.PAYMENT_CHOICES ,widget=forms.Select(attrs={'class': 'form-control'}))
    paid_amount = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    card_no = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    mfs_channel = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserPayments
        fields = ('payment_method', 'paid_amount', 'card_no', 'mfs_channel')
