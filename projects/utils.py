from .models import Project


def get_optimized_projects_queryset(queryset=None):
    """Возвращает оптимизированный queryset проектов с подгрузкой связанных данных."""
    if queryset is None:
        queryset = Project.objects.all()
    return queryset.select_related('owner').prefetch_related('participants')
