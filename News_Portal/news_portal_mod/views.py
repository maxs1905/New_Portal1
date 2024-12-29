from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class PostsList (ListView):
    model = Post
    # Указываем, что нас интересуют только посты типа 'News'
    queryset = Post.objects.filter(post_type='News').order_by('-create_time')
    # Указываем имя шаблона для списка новостей
    template_name = 'news_list.html'
    # Контекстное имя для списка объектов в шаблоне
    context_object_name = 'news'
class PostsDetail(DetailView):
    model = Post
    # Указываем имя шаблона для отображения подробной информации
    template_name = 'news_detail.html'
    # Контекстное имя для отдельного поста
    context_object_name = 'posts'
