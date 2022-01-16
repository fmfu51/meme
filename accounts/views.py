from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

# Create your views here.
def login(request: HttpRequest):
    return render(request, "accounts/login.html", {})