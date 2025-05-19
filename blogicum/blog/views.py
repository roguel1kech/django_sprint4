from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Category
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'image',
            'category',
            'location',
            'is_published',
            'pub_date',
        ]
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


# Index view: show only published posts up to now
def index(request):
    # Show only published posts up to now
    posts = Post.objects.filter(is_published=True, pub_date__lte=timezone.now())
    return render(request, 'blog/index.html', {'posts': posts})


# Post detail view with comment submission
def post_detail(request, id):
    post = get_object_or_404(
        Post,
        pk=id,
        is_published=True,
        pub_date__lte=timezone.now()
    )
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', id=post.id)
    else:
        form = CommentForm()
    return render(
        request,
        'blog/post_detail.html',
        {
            'post': post,
            'comments': comments,
            'comment_form': form
        }
    )


# Category posts view
def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    )
    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
            'current_category': category
        }
    )
def post_create(request):
    # only logged-in users can create
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_detail', id=post.id)
    else:
        form = PostForm()

    return render(request, 'blog/post_create.html', {'form': form})


# User profile view
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(
        author=profile_user,
        is_published=True,
        pub_date__lte=timezone.now()
    )
    return render(
        request,
        'blog/profile.html',
        {'profile_user': profile_user, 'posts': posts}
    )