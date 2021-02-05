
from django.contrib import admin
from django.urls import path, include


from django.conf.urls.static import static
from django.conf import settings
from post.views import (index, blog, post, search, create_post, 
                        edit_post, delete_post)




urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="homepage"),
    path("blog/", blog, name="view-post"),
    path("create/", create_post, name="create-post"),
    path("post/<myid>/", post, name="post-detail"),
    path("post/<myid>/edit/", edit_post, name="edit-post"),
    path("post/<myid>/delete/", delete_post, name="delete-post"),
    path("search/", search, name="search-result"),
    path("tinymce/", include("tinymce.urls")),
    path('accounts/', include('allauth.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
