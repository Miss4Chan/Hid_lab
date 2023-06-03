from django.contrib import admin
from django.urls import path
from blog import views

#
urlpatterns = [
    path('admin/', admin.site.urls),
    path("posts/", views.posts, name="posts"),
    path("profile/", views.profile, name="profile"),
    path("add/post/", views.add, name="add"),
    #path("blockedUsers/", views.blocked, name="blocked")
    #za ova mi treba forma ushte edna za bloked ama rn sum prenervozna za da go praam toa
    #bice bolje
]
