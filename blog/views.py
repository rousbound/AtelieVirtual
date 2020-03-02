from django.shortcuts import render

from blog.models import Post, Comment
from .forms import CommentForm
import os

module_dir = os.path.dirname(__file__)  

def blog_index(request):

    posts = Post.objects.all().order_by('-created_on')
    context = {
        "posts": posts,
            }
    return render(request, "blog_index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter( 
        categories__name__contains=category
            ).order_by( '-created_on')

    context = { "category": category,
                "posts": posts
                    }

    return render(request, "blog_category.html", context)

def get_images(images_name):
    if images_name == None:
        print("Null image name")
        return
    image_list = []
    for filename in os.listdir(module_dir + "/static/img"):
        if images_name in filename:
            image_list.append("img/" + filename)
    return sorted(image_list)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "images_paths": get_images(post.images_name),
    }
    return render(request, "blog_detail.html", context)
