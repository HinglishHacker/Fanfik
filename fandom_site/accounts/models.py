from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

def default_avatar():
    return 'default_avatar.jpg'  # Положи этот файл в media/avatars

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True,)
    avatar = models.ImageField(upload_to='avatars/', default=default_avatar)
    cover = models.ImageField(upload_to='covers/', default='default_cover.jpg')  # Обложка профиля
    bio = models.TextField(blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    def __str__(self):
        return self.username


User = get_user_model()

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers_set', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # Нельзя подписаться дважды

    def __str__(self):
        return f'{self.follower} подписан на {self.following}'
