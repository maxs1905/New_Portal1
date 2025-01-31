from django.urls import path
from . import views
from .views import (
    PostsList, PostsDetail, PostsSearch, PostsCreate
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
urlpatterns = [
    # Путь для страницы со списком новостей
    path('', cache_page(60)(views.PostsList.as_view()), name='news_list'),
    # Путь для страницы с деталями новости
    path('<int:pk>/', cache_page(300)(views.PostsDetail.as_view()), name='news_detail'),
    path('search', views.PostsSearch.as_view(), name='new_search'),
    path('create/', views.PostsCreate.as_view(), name='news_create'),
    path('article/create/', views.PostsCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', views.PostsUpdate.as_view(), name='news_update'),
    path('article/<int:pk>/edit/', views.PostsUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', views.PostDelete.as_view(), name='news_delete'),
    path('article/<int:pk>/delete/', views.PostDelete.as_view(), name='article_delete'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
]