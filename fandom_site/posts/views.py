from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

# Список всех постов
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/post_list.html', {'posts': posts})

# Создание поста
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})

# Редактирование поста
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})

# Удаление поста
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'posts/confirm_delete.html', {'post': post})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.select_related('user').order_by('created_at')
    top_level_comments = comments.filter(parent__isnull=True)
    comment_form = CommentForm()

    can_comment = True  # Поскольку нет поля allow_comments, пусть по умолчанию можно

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post

            # Проверка: если отправляется ответ на комментарий
            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    parent_comment = None

            comment.save()
            return redirect('post_detail', pk=pk)

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'top_level_comments': top_level_comments,
        'comment_form': comment_form,
        'can_comment': can_comment,
    })
# Лайк
@login_required
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Comment

def add_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        # Если это ответ на комментарий, то находим родительский комментарий
        parent_comment = None
        if parent_id:
            parent_comment = Comment.objects.get(id=parent_id)
        
        # Создаем новый комментарий
        Comment.objects.create(
            post=post,
            user=request.user,  # Устанавливаем пользователя
            content=content,
            parent=parent_comment  # Устанавливаем родительский комментарий
        )
        
        return redirect('post_detail', post.pk)

# Удаление комментария
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

# Редактирование комментария
@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user:
        return redirect('post_detail', pk=comment.post.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Комментарий успешно обновлён.")
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'posts/edit_comment.html', {'form': form, 'comment': comment})


@login_required
def toggle_favorite(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.favorites.all():
        post.favorites.remove(request.user)
    else:
        post.favorites.add(request.user)
    return redirect('post_detail', pk=pk)  # Возвращаем обратно к посту
