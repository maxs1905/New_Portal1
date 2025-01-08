import django_filters
from .models import Post
from django import forms

class PostFilter(django_filters.FilterSet):
    title_post = django_filters.CharFilter(lookup_expr='icontains', label='Заголовок')
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains', label='Автор')
    create_time = django_filters.DateFilter(widget=forms.DateInput(attrs={"type": "date"}), label="Дата", lookup_expr='gte')

    class Meta:
        model = Post
        fields = ['author_name', 'title_post', 'create_time']  # Мы не используем Meta.fields, так как фильтры определены вручную