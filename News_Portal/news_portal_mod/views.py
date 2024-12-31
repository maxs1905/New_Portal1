from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
from datetime import datetime

class PostsList (ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news'
    ordering = '-create_time'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_quan'] = None
        return context
class PostsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'
