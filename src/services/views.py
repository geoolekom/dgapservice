from django.shortcuts import render, redirect


def print_view(request):
	return redirect('http://print.mipt.ru')


def laundry(request):
	return redirect('http://stiralka.fopf.mipt.ru')


def food(request):
	return redirect('https://veryfood.ru')
