from django.urls import path
from . import views

# app_name = 'video_stream_app'

urlpatterns = [
    path('', views.home, name="home"),
    path('user_subscription_plans/', views.user_subscription_plans, name="user_subscription_plans"),
    path('admin_home/', views.admin_home, name="admin_home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('admin_logout/', views.admin_logout_view, name="admin_logout"),
    path('video_stream_admin/', views.video_stream_admin, name="video_stream_admin"),
    path('video_stream_admin/subscription_plans/', views.subscription_plan_list,
         name="subscription_plans"),
    path('video_stream_admin/subscription_type_list/', views.subscription_type_list,
         name="subscription_type_list"),
    path('video_stream_admin/user_list/', views.user_list,
         name="user_list"),
    path('video_stream_admin/video_list/', views.video_list,
         name="video_list"),
    path('video_stream_admin/subscriptions/<str:ops>/',
         views.admin_subscription_operation, name="admin_subscription_operation"),
    path('video_stream_admin/subscription_type/<str:ops>/',
         views.admin_subscription_type_operation, name="admin_subscription_type_operation"),
    path('video_stream_admin/user/<str:ops>/',
         views.user_operations, name="user_operations"),
    path('video_stream_admin/videos/<str:ops>/',
         views.admin_video_operation, name="user_operations"),

]
