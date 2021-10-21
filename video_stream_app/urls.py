from django.urls import path
from . import views

# app_name = 'video_stream_app'

urlpatterns = [
    path('', views.home, name="home"),
    path('admin_home/', views.admin_home, name="admin_home"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('admin_logout/', views.admin_logout_view, name="admin_logout"),
    path('video_stream_admin/', views.video_stream_admin, name="video_stream_admin"),
    path('video_stream_admin/subscription_plans/', views.subscription_plan_list,
         name="subscription_plans"),
    path('video_stream_admin/subscriptions/<str:ops>/',
         views.admin_product_operation, name="admin_product_operation"),
]