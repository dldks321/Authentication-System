from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login_page'),
    path('register/', views.register, name='register_page'),
    path('complete/', views.complete, name='complete_page'),
    path('management/', views.management, name='user_management_page'),
]
