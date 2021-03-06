from django.urls import path
from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('login/', views.login, name='login'),
	path('register/', views.register, name='register'),
	path('accountdetails/', views.accountdetails, name='accountdetails'),
	path('loginfail/', views.loginfail, name='loginfail'),
	path('accountdetails/device/<str:devid>', views.device, name='device'),
]
