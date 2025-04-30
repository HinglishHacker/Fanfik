from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, EditProfileForm
from .models import CustomUser, Follow
from posts.models import Post

User = get_user_model()

# Регистрация
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Профиль пользователя
@login_required
def profile_view(request):
    user_posts = request.user.posts.all().order_by('-created_at')
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'posts': user_posts,
    })

# Редактирование профиля
@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

# Выход из аккаунта
@login_required
@require_http_methods(["GET", "POST"])
def custom_logout(request):
    logout(request)
    return redirect('home')

# Домашняя страница
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    if posts.exists():
        return render(request, 'posts/post_list.html', {'posts': posts})
    return render(request, 'home.html')

# Просмотр чужого профиля
def user_profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user_profile).order_by('-created_at')

    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user_profile).exists()

    followers_count = Follow.objects.filter(following=user_profile).count()
    following_count = Follow.objects.filter(follower=user_profile).count()

    return render(request, 'accounts/user_profile.html', {
        'user_profile': user_profile,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    })

# Подписка/отписка
@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)

    if target_user == request.user:
        return redirect('user_profile', username=username)  # нельзя подписаться на себя

    follow_relation = Follow.objects.filter(follower=request.user, following=target_user)

    if follow_relation.exists():
        follow_relation.delete()
    else:
        Follow.objects.create(follower=request.user, following=target_user)

    return redirect('user_profile', username=username)
