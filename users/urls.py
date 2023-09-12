# This code defines the URL patterns for the blog application.

from django.urls import path

from django.contrib.auth import views as auth_views
from .views import (
    home_view, 
    signup_view,
    profile,
    user_logout,
    update,
    UserDelete,
    LoginView,
    activate
    )

urlpatterns = [
    # The login view is used to log in users.
    path('login/', LoginView.as_view(), name='login'),

    # The home view is the home page for the blog application.
    path('', home_view, name='blog-home'),

    # The signup view is used to create new users.
    path('signup/', signup_view, name='signup'),

    # The activate view is used to activate new users.
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    # The logout view is used to log out users.
    path('logout/', user_logout, name='logout'),

    # The profile view is used to view the user's profile.
    path('profile/', profile, name='profile'),

    # The update view is used to update the user's profile.
    path('update/', update, name='update'),

    # The user_delete view is used to delete a user.
    path('user_delete/<int:pk>/', UserDelete.as_view(), name='user_delete'),
]
