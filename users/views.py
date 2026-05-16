from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from core.constants import USERS_PER_PAGE
from projects.models import Project

from .forms import RegisterForm, UserProfileForm
from .models import User

UserModel = get_user_model()


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'

    def get_success_url(self):
        return reverse('projects:project_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Регистрация успешна!')
        return response


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('projects:project_list')

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный email или пароль.')
        return super().form_invalid(form)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change_form.html'

    def get_success_url(self):
        return reverse('users:user_profile', kwargs={'user_id': self.request.user.id})

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменён!')
        return super().form_valid(form)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:user_profile', kwargs={'user_id': self.request.user.id})

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлён!')
        return super().form_valid(form)


def user_logout(request):
    logout(request)
    return redirect('projects:project_list')


def user_list(request):
    users = UserModel.objects.all()
    active_filter = request.GET.get('filter')
    if request.user.is_authenticated:
        if active_filter == 'favorite_authors':
            fav_projects = request.user.favorites.all()
            users = UserModel.objects.filter(owned_projects__in=fav_projects).distinct()
        elif active_filter == 'my_participants':
            my_projects = request.user.participated_projects.all()
            users = UserModel.objects.filter(owned_projects__in=my_projects).distinct()
        elif active_filter == 'liked_my_projects':
            my_projects = Project.objects.filter(owner=request.user)
            users = UserModel.objects.filter(favorites__in=my_projects).distinct()
        elif active_filter == 'my_project_members':
            my_projects = Project.objects.filter(owner=request.user)
            users = UserModel.objects.filter(participated_projects__in=my_projects).distinct()
    paginator = Paginator(users, USERS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/user_list.html', {
        'page_obj': page_obj,
        'active_filter': active_filter
    })


def user_profile(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    return render(request, 'users/user_profile.html', {'user_profile': user_profile})
