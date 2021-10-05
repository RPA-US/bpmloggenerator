from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages

def home_page(request):
    return render(request, "home.html", context)

def termandconds_page(request):
    return render(request, "termandconds.html", {})
