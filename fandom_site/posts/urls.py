from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),  # Главная страница с постами
    path('create/', views.create_post, name='create_post'),  # Создание поста
    path('post/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Детальная страница поста
    path('post/edit/<int:pk>/', views.edit_post, name='edit_post'),  # Редактирование поста
    path('post/delete/<int:pk>/', views.delete_post, name='delete_post'),  # Удаление поста
    path('post/<int:post_pk>/comment/', views.add_comment, name='add_comment'),# Добавить комментарий
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'), 
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
]
