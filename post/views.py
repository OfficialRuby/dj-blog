from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from post.forms import CommentForm, PostForm

from django.shortcuts import render, get_object_or_404, redirect,reverse
from post.models import Post, Author, Post_View
from newsletter.models import Subscriber


def get_category_count():
    queryset = Post.objects.values('category__title').annotate(Count("category__title")) #Value filters all objects in category field
    # Annotate converts the list to a dictionary
    #Count counts the numbers of object in the dictionary
    return queryset

def index(request):
    featured = Post.objects.filter(featured=True) # filter all featured post
    latest = Post.objects.order_by("-timestamp")[0:3] #Sort according to the timestamp
    
    if request.method == "POST":
        email = request.POST['email']
        new_signup = Subscriber()
        new_signup.email = email
        new_signup.save()

    
    context = {
        "object_list" : featured,
        "latest" : latest
    }
    return render(request, "index.html", context)


def blog(request):

    category_count = get_category_count()
    #print (category_count)
    most_recent = Post.objects.order_by("-timestamp") [:3]
    post_list = Post.objects.all()

    paginate = Paginator(post_list, 3)
    page_req_var = 'page'
    page_req = request.GET.get(page_req_var)

    try:
        paginated_queryset = paginate.page(page_req)
    except PageNotAnInteger:
        paginated_queryset = paginate.page(1)
    except EmptyPage:
        paginated_queryset = paginate.page(paginate.num_pages)# Returns the last page in the paginator 



    context =  {
        "queryset" : paginated_queryset,   # queryset
        'page_request_var' : page_req_var,
        "most_recent" : most_recent,
        "category_count": category_count
    }
    return render(request, "blog.html", context)


def post(request, myid):
    post = get_object_or_404(Post, id=myid)
    form = CommentForm(request.POST or None)
    if request.user.is_authenticated:
        Post_View.objects.get_or_create(user=request.user, post=post)

    if request.method== "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post # From post = get_object_or_404(Post, id=myid)
            form.save()
            return redirect(reverse("post-detail", kwargs={
                "myid" : post.id
            }))
        
    category_count = get_category_count()
    most_recent = Post.objects.order_by("-timestamp") [:3]
    
    context = {
        "form": form,
        "post":post,
        "most_recent" : most_recent,
        "category_count": category_count
    }
    return render(request, "post.html", context)

    

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | #  If search query is contained in title
            Q(overview__icontains=query) # If search query is contained in title
        ).distinct() # If search indexes same result select one

    context = {
        "queryset" : queryset
    }

    return render (request, "search_result.html", context)


def get_author(user):
    queryset= Author.objects.filter(user=user)
    if queryset.exists():
        return queryset[0]
    return None



def edit_post(request, myid):
    title = "Edit"
    post = get_object_or_404(Post, id=myid)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)  # Get the Post author 
    if request.method=="POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                "myid": form.instance.id
            }))
    context = {
        "form": form,
        "title": title
    }
    return render(request, "create_post.html", context)


def create_post(request):
    title = "Create"
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)  # Get the Post author 
    if request.method=="POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                "myid": form.instance.id
            }))
    context = {
        "form": form,
        "title": title
    }
    return render(request, "create_post.html", context)


def delete_post(request, myid):
    post = get_object_or_404(Post, id=myid)
    post.delete()
    return(redirect("view-post"))



