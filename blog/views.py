from django.shortcuts import render
from .models import *
from .forms import *
# Create your views here.
def posts(request):
    #context e toa sho go prakjame posle i so django temp lang 
    #se prikazhuva vo html 
    # Od modelot se zemaat objektite dali so all() ili queryset() 
    #Koga praime render go loadame htmlot i kako context mu pushtame podatoci
    #tuka treba da se pushti i za blocked da ne gi gleash posts na tie sho te imaat blokirano
    blocked = Block.objects.filter(blocker__user=request.user).values_list("blocked")
    #ni treba lista na blocked za da mozheme da filtirame i da gi trgneme posts na
    #useri shto ne imaat blokirano
    posts = Post.objects.get_queryset().exclude(user__user____in=blocked)
    return render(request,"posts.html",{"posts": posts})

def profile(request):
    #samiot profil na userot e ova
    user=BlogUser.objects.get(user=request.user)
    posts = Post.objects.filter(author=user)
    return render(request, "profile.html",{"user":user, "posts":posts})

#ni treba forma za add na new post

#nz tochno kako da go approachnam delov so blocked
#valjda treba i za toa forma so submit? zatoa shto treba da se prati deka se naprail block za da se sochuva

def add(request):
    if request.method == "POST":
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False) #ni treba false zatoa shto ushte ne e dodelen user i jademe not null const violated
            post.author = BlogUser.objects.get(user=request.user)
            post.save()
    return render(request,"addPost.html",{"form":PostForm})