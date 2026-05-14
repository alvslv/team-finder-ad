from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', lambda request: redirect('project_list')),
    # Админка
    path('users/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    
    # Главная страница (список проектов) по ТЗ: /project/list/
    path('project/list/', views.project_list, name='project_list'),
    
    # Страница проекта
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:project_id>/complete/', views.project_complete, name='project_complete'),
    
    # Создание проекта
    path('projects/create-project/', views.project_create, name='project_create'),
    
    # Избранное
    path('projects/favorites/', views.favorite_projects, name='favorite_projects'),
    path('projects/<int:project_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    
    # Пользователи
    path('users/list/', views.user_list, name='user_list'),
    path('users/<int:user_id>/', views.user_profile, name='user_profile'),
    
    # Аутентификация
    path('users/register/', views.register, name='register'),
    path('users/login/', views.user_login, name='login'),
    path('users/logout/', views.user_logout, name='logout'),
    path('users/change-password/', views.change_password, name='change_password'),
    path('users/edit-profile/', views.edit_profile, name='edit_profile'),
    path('projects/<int:project_id>/join/', views.join_project, name='join_project'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
