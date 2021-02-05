from django.contrib import admin
from post.models import Category, Post, Author, Comment, Post_View



admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post_View)