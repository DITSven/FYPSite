from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, AddDeviceForm
from .models import User, Device
import json

# Create your views here.
def index(request):
	return render(request, 'index.html')
	
def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			request.session["username"] = form.cleaned_data["username"]
			return redirect('accountdetails')
		else:
			return render(request, 'loginfail.html')
	else:
		form = LoginForm()
		return render(request, 'login.html', {'form': form})

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user_to_save = User()
			user_to_save.username = form.cleaned_data['username']
			user_to_save.email = form.cleaned_data['email']
			user_to_save.password = form.cleaned_data['password']
			user_to_save.save()
			return render(request, 'registersucceed.html')
		else:
			return render(request, 'registerfail.html')
	else:
		form = RegisterForm()
		return render(request, 'register.html', {'form': form})

@login_required
def accountdetails(request):
	if request.method == 'POST':
		form = AddDeviceForm(request.POST)
		newform = AddDeviceForm()
		if form.is_valid():
			username = request.POST.get('username')
			user = User.objects.get(username=username)
			d = form.cleaned_data['deviceid']
			dev = Device.objects.get(deviceid=d)
			dev.deviceid = d
			dev.devicepsw = form.cleaned_data['deviceid']
			dev.username = user
			dev.save()
		devices = Device.objects.filter(username=username)
		context = { 'username': username, 'devices': devices, 'form': newform }
		return render (request, 'accountdetails.html', context)
	else:
		form = AddDeviceForm()
		username = request.session["username"]
		devices = Device.objects.filter(username=username)
		context = { 'username': username, 'devices': devices, 'form': form }
		return render (request, 'accountdetails.html', context)

def loginfail(request):
	return render (request, 'loginfail.html')
