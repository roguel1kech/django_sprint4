from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from blog.models import Post

User = get_user_model()

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        return redirect('profile', username=user.username)
    return render(request, 'registration/registration_form.html', {'form': form})

def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_obj)
    return render(request, 'users/profile.html', {
        'user_obj': user_obj,
        'posts': posts,
    })

@login_required
def profile_edit(request, username):
    if request.user.username != username:
        return redirect('profile', username=username)
    form = UserChangeForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('profile', username=username)
    return render(request, 'users/profile_edit.html', {'form': form})