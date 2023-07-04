from django.shortcuts import render
import random

# Create your views here.

def index(request):
    if request.META.get("HTTP_HX_REQUEST"):
        return render(request, "webapp/partials/paragraph.html", { "context": random.choice(["Flaco Para de cambiar!", "Dale flaco"]) })
    return render(request, "webapp/dashboard.html")