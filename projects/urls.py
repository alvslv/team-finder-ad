from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('<int:project_id>/complete/', views.project_complete, name='project_complete'),
    path('create-project/', views.ProjectCreateView.as_view(), name='project_create'),
    path('favorites/', views.favorite_projects, name='favorite_projects'),
    path('<int:project_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<int:project_id>/join/', views.join_project, name='join_project'),
]
