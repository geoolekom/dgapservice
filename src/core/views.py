from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth

def login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = auth.authenticate(username=username, password=password)
	print(user.get_username())
	if user is not None and user.is_active:
		auth.login(request, user)
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	else:
		return HttpResponseRedirect(request.META['HTTP_REFERER'])

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])
