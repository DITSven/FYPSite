from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, AddDeviceForm, DeviceInstructionForm
from .models import User, Device
import socket
import ssl
import pickle

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
		username = request.POST.get('username')
		if form.is_valid():
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

@login_required
def device(request, devid):
	if request.method == 'POST':
		form = DeviceInstructionForm(request.POST)
		commands = []
		if form.is_valid():
			colour = request.POST.get('colour')
			message = form.cleaned_data['message']
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
			context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
			conn = context.wrap_socket(sock, server_hostname="ServerFYP")
			try:
				conn.connect(('127.0.0.1', 20560))#to be updated when deploying
			except socket.error:
				print('Could not connect socket')
			if(conn.recv(4096).decode() == 'CONNECTED'):
				pass
			else:
				print("Connection error with server discovery")
			conn.send(b'THIS USER')
			pickled_peer = conn.recv(4096)
			peer = pickle.loads(pickled_peer)
			conn.send(b'Peer rec OK')
			conn.close()
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
			context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
			conn = context.wrap_socket(sock, server_hostname="PeerFYP")
			try:
				conn.connect((peer[1], peer[2]))
			except socket.error:
				print('Could not connect socket')
			conn.send(b'USER COM OUT')
			if conn.recv(4096).decode() == 'DEVICE ID?':
				conn.send(devid.encode())
			comlen = int(conn.recv(4096).decode())
			conn.send(b'COMLEN OK')
			for i in range(0, comlen):
				temp_obj = conn.recv(4096)
				temp_element = pickle.loads(temp_obj)
				if (temp_element == 'EOF'):
					print("EOF")
					break
				commands.append(temp_element)
				conn.send(b'Command Received')
			if conn.recv(4096).decode() == 'SEND COMMAAND':
				pass
			sendcolour = [devid, commands[3] , colour]
			sendmessage =[devid, commands[4] , message]
			psc = pickle.dumps(sendcolour)
			psm = pickle.dumps(sendmessage)
			conn.send(psc)
			if conn.recv(4096).decode() == 'OK':
				conn.send(psm)
			conn.close()			
		return redirect('/usercontrols/accountdetails')
	else:
		form = DeviceInstructionForm()
		commands = []
		cache = []
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
		context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
		conn = context.wrap_socket(sock, server_hostname="ServerFYP")
		try:
			conn.connect(('127.0.0.1', 20560))#to be updated when deploying
		except socket.error:
			print('Could not connect socket')
		if(conn.recv(4096).decode() == 'CONNECTED'):
			pass
		else:
			print("Connection error with server discovery")
		conn.send(b'THIS USER')
		pickled_peer = conn.recv(4096)
		peer = pickle.loads(pickled_peer)
		conn.send(b'Peer rec OK')
		conn.close()
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
		context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
		conn = context.wrap_socket(sock, server_hostname="PeerFYP")
		try:
			conn.connect((peer[1], peer[2]))
		except socket.error:
			print('Could not connect socket')
		conn.send(b'USER COM IN')
		if conn.recv(4096).decode() == 'DEVICE ID?':
			conn.send(devid.encode())
		comlen = int(conn.recv(4096).decode())
		conn.send(b'COMLEN OK')
		for i in range(0, comlen):
			temp_obj = conn.recv(4096)
			temp_element = pickle.loads(temp_obj)
			if (temp_element == 'EOF'):
				break
			commands.append(temp_element)
			print(commands)
			conn.send(b'Command Received')
		iscached = conn.recv(4096).decode()
		comdict = { "SEND_RNG": commands[0], "SEND_TIME": commands[1], "SEND_CONNECTION": commands[2], "GET_COLOUR": commands[3], "GET_MESSAGE": commands[4]}
		if iscached == 'NO CACHE':
			conn.shutdown(socket.SHUT_RDWR)
			conn.close()
			return render (request, 'device.html', {'deviceid': devid, 'commands': comdict, 'cache':[], 'form': form}) 
		else:
			conn.send(b'OK')
		cachelen = int(conn.recv(4096).decode())
		conn.send(b'CACHE LEN OK')
		for i in range(0, cachelen):
			temp_obj = conn.recv(4096)
			temp_element = pickle.loads(temp_obj)
			if (temp_element == 'EOF'):
				break
			cache.append(temp_element)
			conn.send(b'Cache element Received')
		conn.shutdown(socket.SHUT_RDWR)
		conn.close()
		return render (request, 'device.html', {'deviceid': devid, 'commands': comdict, 'cache':cache, 'form': form}) 
