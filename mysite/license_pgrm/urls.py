from . import views
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('', views.indexView, name="home"),
    path('dashboard/',views.dashboardView,name="dashboard"),
    path('login/',LoginView.as_view(), name="login"),
    path("register/", views.signup, name="register_url"),
    path('logout/',LogoutView.as_view(next_page="login"), name="logout"),
    path("create_license", views.create_license, name="create_license"),
]