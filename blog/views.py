from django.shortcuts import render
from .models import *
# Create your views here.
def posts(request):
    #context e toa sho go prakjame posle i so django temp lang 
    #se prikazhuva vo html 
    context = {"posts":Post.objects.get_queryset()}
    return render(request,"posts.html")