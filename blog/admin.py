from typing import Any, Optional
from django.contrib import admin
from django.http.request import HttpRequest
from .models import *

from rangefilter.filter import DateTimeRangeFilter,DateRangeFilter

# Register your models here.

class BlogUserAdmin(admin.ModelAdmin):
    #mozhe li da go menuva, but can edit only his profile data
    def has_change_permissions(self,request,obj=None):
        if  request.user.is_superuser or (obj.user == request.user and obj):
            return True
        else:
            return False
    #mozhe li da go glea,  Each user can see the basic data for all other users
    def has_view_permission(self,request, obj=None): 
        return True
    
        #sam mozhe da si brishe i super 
    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        if request.user.is_superuser or (obj and request.user == obj.blocker.user):
            return True
        return False
    #def has_delete_permission(self,request, obj,form ,change):
     #   if request.user.is_superuser or (obj and request.user == obj.blocker.user):
      #      return True
       # return False
        
    #registration will be possible only for the admin user.
    def has_add_permission(self, request: HttpRequest) -> bool:
        return request.user.is_superuser
    


#ke probam da se dodavaat komentari preku inline kako da se del od post 
class CommentAdmin(admin.ModelAdmin):
    #Each comment is displayed along with its content and the corresponding date it was posted
    list_display = ['content','commentDate']
    #Every user with access to a particular post can write comments on that post
    #see the comments that other users have written on that post
    def has_view_permission(self,request, obj=None): 
         if  request.user.is_superuser or (obj and not Block.objects.filter(blocker=obj.user,blocked=request.user).exists()):
            return True
        
    exclude= ['commenter']
    #mora vaka so save da se stai deka logged in e toj sho go kreaira + zadolzhitelno e toa pole
    def save_model(self,request, obj,form ,change):
        if obj:
            obj.commenter = BlogUser.objects.get(user=request.user)
        super().save_model(request, obj, form, change)

    #The user who wrote the comment and the
    #author who wrote the post to which the comment refers have the option to delete the comment.
    def has_delete_permission(self, request: HttpRequest, obj: Any | None = ...) -> bool:
        if request.user.is_superuser or (obj and request.user == obj.blocker.user):
            return True
        return False

    def has_add_permission(self,request, obj=None):
        return True
    
    def has_change_permission(self,request, obj=None):
        if  request.user.is_superuser or (obj.user == request.user and obj):
            return True
        else:
            return False

class CommentPostAdmin(admin.TabularInline):
    #koga e linine bara user nz kako da go resham toa lol probav so save i pagja
    model = Comment
    extra = 0
    
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentPostAdmin]
    #The blog posts are displayed with their title and author
    list_display = ['title','author']
    #user can filter posts by creation date, using a from-to time interval
    list_filter = ["creationDate","modificationDate"]
    #the user can search the posts by their title and content.
    search_fields = ['title','content']

    #sakame userot shto e logiran da bide user na postot aka avtomatski da se stava po logged in
    exclude= ['author']
    #mora vaka so save da se stai deka logged in e toj sho go kreaira + zadolzhitelno e toa pole
    def save_model(self,request, obj,form ,change):
        if obj:
            obj.author = BlogUser.objects.get(user=request.user)
        super().save_model(request, obj, form, change)

    #Only the author of the post can edit it
    def has_change_permission(self,request, obj=None):
        if  request.user.is_superuser or (obj.user == request.user and obj):
            return True
        else:
            return False
        
    # while all other users can see the posts, 
    # blocked user will no longer be able to see the posts written by the user who blockedthem. 
    def has_view_permission(self,request, obj=None): 
        if  request.user.is_superuser or (obj and not Block.objects.filter(blocker=obj.user,blocked=request.user).exists()):
            #baraj u blocked ako ima mesto kaj sho userot na objektot go ima blokirano onoj sho saka access
            return True
        
    def has_add_permission(self,request, obj=None):
        return True


class BlockAdmin(admin.ModelAdmin):
    def has_view_permission(self,request, obj=None):
        if  request.user.is_superuser or (obj.user == request.user and obj):
            return True
        else:
            return False

    def has_change_permission(self,request, obj=None):
        if  request.user.is_superuser or (obj.user == request.user and obj):
            return True
        return False

    #def has_delete_permission(self,request, obj,form ,change):
    #    if obj and request.user == obj.blocker.user:
    #        return True
    #    return False

    def has_add_permission(self,request, obj=None):
        return True


admin.site.register(BlogUser, BlogUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Block,BlockAdmin)