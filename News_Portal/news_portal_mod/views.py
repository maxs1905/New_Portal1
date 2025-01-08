from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy

class PostsList(ListView):
    model = Post
    template_name = 'news_list.html'
    context_object_name = 'news'
    ordering = '-create_time'
    paginate_by = 2

class PostsSearch(PostsList):
    template_name = 'news_search.html'
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'

class PostsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'posts_edit.html'

    def form_valid(self, form):
        if self.request.path.startswith('/news/create/'):
            form.instance.post_type = 'News'
        elif self.request.path.startswith('/article/create/'):
            form.instance.post_type = 'Article'
        return super().form_valid(form)
class PostsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'posts_edit.html'
    def form_valid(self, form):
        if self.request.path.startswith('/news/create/'):
            form.instance.post_type = 'News'
        elif self.request.path.startswith('/article/create/'):
            form.instance.post_type = 'Article'
        return super().form_valid(form)

class PostDelete(DeleteView):
    model = Post
    template_name = 'posts_delete.html'
    success_url = reverse_lazy('news_list')