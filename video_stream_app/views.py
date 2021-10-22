from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse

from .forms import (SubscriptionForm, UserRegistrationForm, UserLoginForm, SubscriptionTypeForm, UserEditForm,
                    VideoContentUploadForm)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models


@login_required(login_url='/login/')
def home(request):
    return render(request, 'video_stream_app/home_page.html',
                  {
                      'is_logged_in': request.user.is_authenticated,
                      'home': 'active'
                  })


@login_required(login_url='/video_stream_admin/')
def admin_home(request):
    return render(request, 'video_stream_app/admin_home.html',
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


@login_required(login_url='/video_stream_admin/')
def subscription_plan_list(request):
    return render(request, 'video_stream_app/subscriptions.html',
                  {
                      'subscriptions': models.Subscription.objects.all(),
                      'title': 'Available Plans',
                      'is_logged_in': request.user.is_authenticated,
                      'subscription_plans': 'active',
                      'admin': True
                  })


@login_required(login_url='/video_stream_admin/')
def subscription_type_list(request):
    return render(request, 'video_stream_app/subscription_type.html',
                  {
                      'subscription_type_lst': models.SubscriptionType.objects.all(),
                      'title': 'Available Plans',
                      'is_logged_in': request.user.is_authenticated,
                      'subscription_types': 'active',
                      'admin': True
                  })


@login_required(login_url='/video_stream_admin/')
def user_list(request):
    return render(request, 'video_stream_app/users_view.html',
                  {
                      'users': models.User.objects.all(),
                      'title': 'Users',
                      'is_logged_in': request.user.is_authenticated,
                      'users_link': 'active',
                      'admin': True
                  })


@login_required(login_url='/video_stream_admin/')
def video_list(request):
    return render(request, 'video_stream_app/videos.html',
                  {
                      'videos': models.VideoContent.objects.all(),
                      'title': 'Videos',
                      'is_logged_in': request.user.is_authenticated,
                      'video_link': 'active',
                      'admin': True
                  })


@login_required(login_url='/video_stream_admin/')
def admin_subscription_operation(request, ops):
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
            subs_id = ops.split('__')[-1]
            subscription = models.Subscription.objects.filter(pk=subs_id).first()
            form = SubscriptionForm(request.POST, instance=subscription)
            if form.is_valid():
                form.save()
                messages.success(request, "Succesfully Updated.")
            else:
                messages.error(request, "Something Went Wrong.")
            return redirect("subscription_plans")

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
            subs_id = ops.split('__')[-1]
            subs = models.Subscription.objects.filter(pk=subs_id).first()
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
        elif 'delete' in ops:
            subs_id = ops.split('__')[-1]
            # return JsonResponse(cat_id, safe=False)
            _ = models.Subscription.objects.filter(pk=subs_id).delete()
            return redirect("subscription_plans")
        else:
            return redirect("subscription_plans")


@login_required(login_url='/video_stream_admin/')
def admin_subscription_type_operation(request, ops):
    if request.method == "POST":
        if ops == 'add':
            form = SubscriptionTypeForm(request.POST)
            if form.is_valid():
                messages.success(request, "Succesfully added.")
                form.save()
            else:
                messages.error(request, "Something Went Wrong.")
                return redirect("video_stream_admin/subscription_type/add/")
            return redirect("/video_stream_admin/subscription_type/add/")
        elif 'edit' in ops:
            subs_id = ops.split('__')[-1]
            subscription_type = models.SubscriptionType.objects.filter(pk=subs_id).first()
            form = SubscriptionTypeForm(request.POST, instance=subscription_type)
            if form.is_valid():
                form.save()
                messages.success(request, "Succesfully Updated.")
            else:
                messages.error(request, "Something Went Wrong.")
            return redirect("subscription_type_list")

    elif request.method == 'GET':
        if ops == 'add':
            form = SubscriptionTypeForm()
            return render(request, "video_stream_app/all_forms.html",
                          context={"is_logged_in": request.user.is_authenticated,
                                   "form": form,
                                   "title": "Add Subscription Type",
                                   "admin": 1,
                                   'logout': request.user.is_authenticated,
                                   "btn_name": "ADD Subscription Type",
                                   "subscription_types": "active"})
        elif 'edit' in ops:
            subs_id = ops.split('__')[-1]
            subs_type = models.SubscriptionType.objects.filter(pk=subs_id).first()
            form = SubscriptionTypeForm(initial={"type_name": subs_type.type_name})

            return render(request, "video_stream_app/all_forms.html",
                          context={'is_logged_in': request.user.is_authenticated,
                                   "form": form,
                                   "title": "Edit Subscription Type",
                                   "admin": True,
                                   'logout': request.user.is_authenticated,
                                   "btn_name": "Edit Subscription Type",
                                   "subscription_types": "active"})
        elif 'delete' in ops:
            sub_types_id = ops.split('__')[-1]
            # return JsonResponse(cat_id, safe=False)
            _ = models.SubscriptionType.objects.filter(pk=sub_types_id).delete()
            return redirect("subscription_type_list")
        else:
            return redirect("subscription_type_list")


@login_required(login_url='/video_stream_admin/')
def user_operations(request, ops):
    if request.method == "GET":
        if 'edit' in ops:
            user_id = ops.split('__')[-1]
            user = models.User.objects.filter(pk=user_id).first()
            form = UserEditForm(initial={
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "user_subscription": user.user_subscription,
                "user_type": user.user_type,
                "is_subscribed": user.is_subscribed,
                "is_blocked": user.is_blocked,
                "purchase_date": user.purchase_date,
            })

            return render(request, "video_stream_app/all_forms.html",
                          context={'is_logged_in': request.user.is_authenticated,
                                   "form": form,
                                   "title": "Edit User",
                                   "admin": True,
                                   'logout': request.user.is_authenticated,
                                   "btn_name": "Edit User",
                                   "users_link": "active"})
        elif 'delete' in ops:
            user_id = ops.split('__')[-1]
            # return JsonResponse(cat_id, safe=False)
            _ = models.User.objects.filter(pk=user_id).delete()
            return redirect("user_list")
    elif request.method == "POST":
        if 'edit' in ops:
            user_id = ops.split('__')[-1]
            user = models.User.objects.filter(pk=user_id).first()
            form = UserEditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Succesfully Updated.")
            else:
                messages.error(request, "Something Went Wrong.")
            return redirect("user_list")

        elif 'delete' in ops:
            user_id = ops.split('__')[-1]
            # return JsonResponse(cat_id, safe=False)
            _ = models.User.objects.filter(pk=user_id).delete()
            return JsonResponse(1, safe=False)

    return redirect("user_list")


@login_required(login_url='/video_stream_admin/')
def admin_video_operation(request, ops):
    if request.method == "POST":
        if ops == 'add':
            data = None
            # form = VideoContentUploadForm(request.POST, request.FILES)
            # # print(form.is_valid())
            # if form.is_valid():
            #     messages.success(request, "Succesfully added.")
            #     form.save()
            # else:
            #     messages.error(request, "Something Went Wrong.")
            return redirect("video_list")
        elif 'edit' in ops:
            subs_id = ops.split('__')[-1]
            subscription = models.Subscription.objects.filter(pk=subs_id).first()
            form = SubscriptionForm(request.POST, instance=subscription)
            if form.is_valid():
                form.save()
                messages.success(request, "Succesfully Updated.")
            else:
                messages.error(request, "Something Went Wrong.")
            return redirect("subscription_plans")

    elif request.method == 'GET':
        if ops == 'add':
            form = VideoContentUploadForm()
            return render(request, "video_stream_app/all_forms.html",
                          context={"is_logged_in": request.user.is_authenticated,
                                   "form": form,
                                   "title": "Add Video",
                                   "admin": 1,
                                   'logout': request.user.is_authenticated,
                                   "btn_name": "ADD Video",
                                   "video_link": "active"})
        elif 'edit' in ops:
            subs_id = ops.split('__')[-1]
            subs = models.Subscription.objects.filter(pk=subs_id).first()
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
        elif 'delete' in ops:
            subs_id = ops.split('__')[-1]
            # return JsonResponse(cat_id, safe=False)
            _ = models.Subscription.objects.filter(pk=subs_id).delete()
            return redirect("video_list")
        else:
            return redirect("video_list")
