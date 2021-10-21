from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from .models import Subscription, SubscriptionType, User


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=255, help_text='Required. Inform a valid email address.',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    full_name = forms.CharField(max_length=15, required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control'}))

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
    password = forms.PasswordInput()

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
