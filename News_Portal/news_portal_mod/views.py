from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View


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

class PostsCreate( PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'posts_edit.html'
    permission_required = 'news.add_post'

    def form_valid(self, form):
        if self.request.path.startswith('/news/create/'):
            form.instance.post_type = 'News'
        elif self.request.path.startswith('/news/article/create/'):
            form.instance.post_type = 'Article'
        return super().form_valid(form)
class PostsUpdate(PermissionRequiredMixin, UpdateView, LoginRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'posts_edit.html'
    permission_required = 'news.change_post'

    login_url = '/login/'
    def form_valid(self, form):
        if self.request.path.startswith('/news/edit/'):
            form.instance.post_type = 'News'
        elif self.request.path.startswith('/news/article/edit/'):
            form.instance.post_type = 'Article'
        return super().form_valid(form)

class PostDelete(DeleteView):
    model = Post
    template_name = 'posts_delete.html'
    success_url = reverse_lazy('news_list')

class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')
class SubscribeView(View):
    def get(self, request):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'category_detail.html', context)
    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        category.subscribers.add(request.user)
        return redirect('subscribe')
