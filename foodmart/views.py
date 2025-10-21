# foodmart/views.py
from django.shortcuts import render

def foodmart_home(request):
    return render(request, 'foodmart/index.html')

def women_view(request):
    return render(request, 'foodmart/women.html')
