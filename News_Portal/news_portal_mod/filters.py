import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    # Фильтр по заголовку поста (с использованием icontains для поиска по подстроке)
    title_post = django_filters.CharFilter(lookup_expr='icontains', label='Заголовок')
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains', label='Автор')
    create_time = django_filters.DateTimeFilter(lookup_expr='gte', label='Дата публикации (с)')

    class Meta:
        model = Post
        fields = ['author_name', 'title_post', 'create_time']  # Мы не используем Meta.fields, так как фильтры определены вручную