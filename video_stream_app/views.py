from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import (SubscriptionForm, UserRegistrationForm, UserLoginForm)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, Count
from django.db.utils import IntegrityError
from . import models
from django.http import JsonResponse, response
import json
import os
from django.conf import settings
from django.http import FileResponse, Http404


@login_required(login_url='/login/')
def home(request):
    return render(request, 'home_page.html',
                  {
                      'is_logged_in': request.user.is_authenticated,
                      'home': 'active'
                  })


@login_required(login_url='/video_stream_admin/')
def admin_home(request):
    return render(request, 'admin_home.html',
                  {
                      'is_logged_in': request.user.is_authenticated,
                      "admin": 1,
                      "admin_home": "active"
                  })


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = UserRegistrationForm()
            return render(request, 'video_stream_app/all_forms.html', {'form': form,
                                                                       "btn_name": "SignUp",
                                                                       "title": "Sign Up",
                                                                       "signup": "active"})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = UserLoginForm()
            return render(request, "video_stream_app/all_forms.html", context={"form": form,
                                                                               "btn_name": "Login",
                                                                               "title": "Login",
                                                                               "login": "active"})


def logout_view(request):
    logout(request)
    return redirect('login')


def admin_logout_view(request):
    logout(request)
    return redirect('video_stream_admin')


def video_stream_admin(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    messages.info(
                        request, f"You are now logged in as {username}.")
                    if request.GET.get('next', None):
                        return redirect(request.GET.get('next'))
                    return redirect("admin_home")
                else:
                    messages.error(request, "You are not a superuser")
                    return redirect("video_stream_admin")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    elif request.method == 'GET':
        if request.user.is_authenticated and request.user.is_superuser:
            if request.GET.get('next', None):
                return redirect(request.GET.get('next'))
            return redirect('admin_home')
        else:
            form = UserLoginForm()
            return render(request, "video_stream_app/all_forms.html", context={"form": form,
                                                                               "btn_name": "Login",
                                                                               "title": "Admin Login",
                                                                               "admin_login": "active"})


@login_required(login_url='/login/')
def subscription_plan_list(request):
    return render(request, 'subscriptions.html',
                  {
                      'subscriptions': models.Subscription.objects.all(),
                      'title': 'Available Plans',
                      'is_logged_in': request.user.is_authenticated,
                      'home': 'active',
                      'admin': True
                  })


@login_required(login_url='/video_stream_admin/')
def admin_product_operation(request, ops):
    if request.method == "POST":
        if ops == 'add':
            form = SubscriptionForm(request.POST)
            if form.is_valid():
                messages.success(request, "Succesfully added.")
                form.save()
            else:
                messages.error(request, "Something Went Wrong.")
            return redirect("/video_stream_admin/subscriptions/add/")
        elif 'edit' in ops:
            cat_id = ops.split('__')[-1]
            cat = models.Subscription.objects.filter(pk=cat_id).first()
            form = SubscriptionForm(request.POST, instance=cat)
            if form.is_valid():
                form.save()
                messages.success(request, "Succesfully Updated.")
            else:
                messages.error(request, "Something Went Wrong.")
            return redirect("/video_stream_admin/subscription_plans/")
        elif 'delete' in ops:
            prod_id = ops.split('__')[-1]
            # return JsonResponse(cat_id, safe=False)
            cat = models.Subscription.objects.filter(pk=prod_id).delete()
            return JsonResponse(1, safe=False)

    elif request.method == 'GET':
        if ops == 'add':
            form = SubscriptionForm()
            return render(request, "video_stream_app/all_forms.html",
                          context={"is_logged_in": request.user.is_authenticated,
                                   "form": form,
                                   "title": "Add Subscription",
                                   "admin": 1,
                                   'logout': request.user.is_authenticated,
                                   "btn_name": "ADD Subscription",
                                   "subscription_plans": "active"})
        elif 'edit' in ops:
            prod_id = ops.split('__')[-1]
            subs = models.Subscription.objects.filter(pk=prod_id).first()
            form = SubscriptionForm(initial={"subscription_type": subs.subscription_type,
                                             "subscription_price": subs.subscription_price,
                                             "subscription_validity": subs.subscription_validity
                                             })
            return render(request, "video_stream_app/all_forms.html",
                          context={'is_logged_in': request.user.is_authenticated,
                                   "form": form,
                                   "title": "Edit Subscription",
                                   "admin": True,
                                   'logout': request.user.is_authenticated,
                                   "btn_name": "Edit Subscription",
                                   "subscription_plans": "active"})
        else:
            return redirect("admin_product")
