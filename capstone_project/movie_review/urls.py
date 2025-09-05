"""
URL configuration for capstone_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from movie_review import views
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, AdminCreateUserAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", LoginView.as_view(template_name='movie_review/login.html'), name='login_html'),
    path("logout/", LogoutView.as_view(template_name='movie_review/logout.html'), name='logout_html'),
    path("register/", views.RegisterView.as_view(template_name='movie_review/register.html'), name='register_html'),
    path('api/auth/register/', RegisterAPIView.as_view(), name='register_api'),
    path('api/auth/login/', LoginAPIView.as_view(), name='login_api'),
    path('api/auth/logout/', LogoutAPIView.as_view(), name='logout_api'),
    path('api/admin/create/', AdminCreateUserAPIView.as_view(), name='create_admin'),
    path('api/movies/', views.MovieListCreateAPIView.as_view(), name='movie_list_api'),
    path('api/movies/<str:title>/', views.MovieRetrieveUpdateDestroyAPIView.as_view(), name='movie_detail'),
    path('api/movies/<str:title>/reviews/', views.ReviewListCreateAPIView.as_view(), name='review-list'),
    path('api/reviews/<int:pk>/', views.ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-detail')

]