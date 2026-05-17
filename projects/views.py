from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from core.constants import STATUS_CLOSED, STATUS_OPEN
from core.services import paginate

from .forms import ProjectForm
from .models import Project
from .utils import get_optimized_projects_queryset


def project_list(request):
    projects = get_optimized_projects_queryset().all()
    favorites_ids = []
    if request.user.is_authenticated:
        favorites_ids = request.user.favorites.values_list('id', flat=True)
    page_obj = paginate(request, projects)
    return render(request, 'projects/project_list.html', {
        'page_obj': page_obj,
        'favorites_ids': list(favorites_ids),
    })


def project_detail(request, project_id):
    project = get_object_or_404(get_optimized_projects_queryset(), id=project_id)
    return render(request, 'projects/project-details.html', {'project': project})


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        form.instance.participants.add(self.request.user)
        messages.success(self.request, 'Проект успешно создан!')
        return response

    def get_success_url(self):
        return reverse('projects:project_detail', kwargs={'project_id': self.object.id})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Проект обновлён!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('projects:project_detail', kwargs={'project_id': self.object.id})


@login_required
def project_complete(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if project.status == STATUS_OPEN:
        project.status = STATUS_CLOSED
        project.save()
        messages.success(request, f'Проект "{project.name}" завершён!')
    return redirect('projects:project_detail', project_id=project.id)


@login_required
def favorite_projects(request):
    favorites = get_optimized_projects_queryset(request.user.favorites.all())
    return render(request, 'projects/favorite_projects.html', {'favorites': favorites})


@login_required
def toggle_favorite(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    is_favorite = request.user.favorites.filter(id=project_id).exists()
    if is_favorite:
        request.user.favorites.remove(project)
    else:
        request.user.favorites.add(project)
    return JsonResponse({'status': 'ok', 'favorited': not is_favorite})


@login_required
def join_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user == project.owner:
        messages.error(request, 'Вы не можете присоединиться к своему проекту.')
    elif project.participants.filter(id=request.user.id).exists():
        project.participants.remove(request.user)
        messages.success(request, f'Вы покинули проект "{project.name}".')
    else:
        project.participants.add(request.user)
        messages.success(request, f'Вы присоединились к проекту "{project.name}"!')
    return redirect('projects:project_detail', project_id=project.id)
