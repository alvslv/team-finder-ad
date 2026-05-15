from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('list/', views.user_list, name='user_list'),
    path('<int:user_id>/', views.user_profile, name='user_profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('edit-profile/', views.UserProfileUpdateView.as_view(), name='edit_profile'),
]
