from django.shortcuts import render, redirect


# Create your views here.
def homePage(request):
    return render(request, 'store/main.html')