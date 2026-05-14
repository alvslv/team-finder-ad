from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import User, Project
from .forms import RegisterForm, ProjectForm


def project_list(request):
    """Главная страница - список проектов"""
    projects = Project.objects.all().order_by('-created_at')
    
    favorites_ids = []
    if request.user.is_authenticated:
        favorites_ids = request.user.favorites.values_list('id', flat=True)
    
    return render(request, 'projects/project_list.html', {
        'projects': projects,
        'favorites_ids': list(favorites_ids),
    })

def project_detail(request, project_id):
    """Страница проекта"""
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def project_create(request):
    """Создание проекта"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            messages.success(request, 'Проект успешно создан!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'projects/create-project.html', {'form': form})


@login_required

@login_required
def project_complete(request, project_id):
    """Завершение проекта"""
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if project.status == 'open':
        project.status = 'closed'
        project.save()
        messages.success(request, f'Проект "{project.name}" завершён!')
    return redirect('project_detail', project_id=project.id)


@login_required
def favorite_projects(request):
    """Страница избранного"""
    favorites = request.user.favorites.all()
    return render(request, 'projects/favorite_projects.html', {'favorites': favorites})


@login_required
def toggle_favorite(request, project_id):
    """Добавление/удаление из избранного"""
    project = get_object_or_404(Project, id=project_id)
    if project in request.user.favorites.all():
        request.user.favorites.remove(project)
        is_favorite = False
    else:
        request.user.favorites.add(project)
        is_favorite = True
    return JsonResponse({'status': 'ok', 'favorited': is_favorite})



def user_profile(request, user_id):
    """Профиль пользователя"""
    user_profile = get_object_or_404(User, id=user_id)
    return render(request, 'users/user_profile.html', {'user_profile': user_profile})


def register(request):
    """Регистрация"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('project_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    """Вход"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('project_list')
        else:
            messages.error(request, 'Неверный email или пароль.')
    return render(request, 'registration/login.html')


def user_logout(request):
    """Выход"""
    logout(request)
    return redirect('project_list')


@login_required
def change_password(request):
    """Смена пароля"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пароль успешно изменён!')
            return redirect('user_profile', user_id=request.user.id)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})

@login_required
def project_edit(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Проект обновлён!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': True,
        'project': project
    })

@login_required
def edit_profile(request):
    from django import forms
    
    class UserProfileForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']
            labels = {
                'name': 'Имя',
                'surname': 'Фамилия',
                'avatar': 'Аватар (URL)',
                'about': 'О себе',
                'phone': 'Телефон',
                'github_url': 'GitHub',
            }
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('user_profile', user_id=request.user.id)
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/edit_profile.html', {'form': form})


def user_list(request):
    """Список пользователей с фильтрацией (вариант 1)"""
    from .models import User, Project
    
    users = User.objects.all()
    active_filter = request.GET.get('filter')
    
    if request.user.is_authenticated:
        if active_filter == 'favorite_authors':
            # 1. Авторы избранных проектов
            fav_projects = request.user.favorites.all()
            users = User.objects.filter(owned_projects__in=fav_projects).distinct()
        elif active_filter == 'my_participants':
            # 2. Авторы проектов, в которых я участвую
            my_projects = request.user.participated_projects.all()
            users = User.objects.filter(owned_projects__in=my_projects).distinct()
        elif active_filter == 'liked_my_projects':
            # 3. Пользователи, которым нравятся мои проекты
            my_projects = Project.objects.filter(owner=request.user)
            users = User.objects.filter(favorites__in=my_projects).distinct()
        elif active_filter == 'my_project_members':
            # 4. Участники моих проектов
            my_projects = Project.objects.filter(owner=request.user)
            users = User.objects.filter(participated_projects__in=my_projects).distinct()
    
    return render(request, 'users/user_list.html', {
        'users': users,
        'active_filter': active_filter
    })

@login_required
def join_project(request, project_id):
    from django.shortcuts import get_object_or_404
    from django.contrib import messages
    from .models import Project
    
    project = get_object_or_404(Project, id=project_id)
    
    if request.user == project.owner:
        messages.error(request, 'Вы не можете присоединиться к своему проекту.')
    elif request.user in project.participants.all():
        project.participants.remove(request.user)
        messages.success(request, f'Вы покинули проект "{project.name}".')
    else:
        project.participants.add(request.user)
        messages.success(request, f'Вы присоединились к проекту "{project.name}"!')
    
    return redirect('project_detail', project_id=project.id)
