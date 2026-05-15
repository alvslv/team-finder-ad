from .models import Project


def get_optimized_projects_queryset():
    """Возвращает оптимизированный queryset проектов с подгрузкой связанных данных."""
    return Project.objects.select_related('owner').prefetch_related('participants')
