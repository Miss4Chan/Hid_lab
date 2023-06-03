from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    #od django bratot ide ova user ez ima unutra se sho sakash i nekjesh
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE) 
    content = models.TextField()
    #files???
    creationDate = models.DateTimeField(auto_now_add=True) #koga prv pat ke se kreira
    modificationDate = models.DateTimeField(auto_now=True) #go stava sekoj pat koga ima save

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField()
    commenter = models.ForeignKey(BlogUser, on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.commenter.user.username+ " " + str(self.commentDate.date)
    
class Block(models.Model):
    blocker = models.ForeignKey(BlogUser, on_delete=models.CASCADE,related_name="blocker")
    blocked = models.ForeignKey(BlogUser, on_delete=models.CASCADE,related_name="blocked")

    def __str__(self):
        return self.blocker +" "+ self.blocked

class File(models.Model):
    file = models.FileField(upload_to="files/")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name
    
