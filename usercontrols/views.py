from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from .models import User, Device

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
	username = request.session["username"]
	devices = Device.objects.filter(user=username)
	context = { 'username': username, 'devices': devices }
	return render (request, 'accountdetails.html', context)

def loginfail(request):
	return render (request, 'loginfail.html')
