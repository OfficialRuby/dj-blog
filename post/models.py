from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from tinymce import HTMLField


USER = get_user_model()




#Post author information
class Author(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username
        
# Post category.

class Category(models.Model):
    title = models.CharField(max_length = 20)
    
    def __str__(self):
        return self.title




class Post_View(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE) # Post was called before definition

    def __str__(self):
        return self.user.username






class Comment(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE) #Post called before definition


    def __str__(self):
        return self.user.username





#Post content

class Post(models.Model):
    title = models.CharField(max_length=80)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #comment_count =models.IntegerField(default=0)
    #view_count =models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    category = models.ManyToManyField(Category)
    featured = models.BooleanField()
    #content = HTMLField()
    previous_post = models.ForeignKey("self", related_name="previous", on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey("self", related_name="next", on_delete=models.SET_NULL, blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    
    

    def get_absolute_url(self):
        return reverse("post-detail", kwargs ={
            "myid": self.id
        })



    def create_post(self):
        return reverse("create-post", kwargs ={
            "myid": self.id
        })


    def update_post(self):
        return reverse("update-post", kwargs ={
            "myid": self.id
        })


    def delete_post(self):
        return reverse("delete-post", kwargs ={
            "myid": self.id
        })

    @property
    def view_count(self):
        return Post_View.objects.filter(post=self).count()



    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()



    @property
    def get_comments(self):
        return self.comments.all().order_by("-timestamp")
    
    

    def __str__(self):
        return self.title

    

