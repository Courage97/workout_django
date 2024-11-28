from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('fitness', views.fitness, name='fitness'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('update_exercise/', views.update_exercise, name='update_exercise'),
]
