from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_logout
from .views import user_profile_view

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('user/<str:username>/', user_profile_view, name='user_profile'),
    path('follow/<str:username>/', views.toggle_follow, name='toggle_follow'),
]
