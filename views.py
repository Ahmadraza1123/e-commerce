# E_Commerce/views.py

from django.shortcuts import render  # 👈 render function import karna zaruri hai

# Home page view (index.html)
def foodmart_home(request):
    return render(request, 'foodmart/index.html')

# Women page view (women.html)
def women_view(request):
    return render(request, 'foodmart/women.html')
