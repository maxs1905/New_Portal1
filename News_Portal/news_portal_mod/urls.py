from django.urls import path
from . import views
from .views import (
    PostsList, PostsDetail, PostsSearch, PostsCreate
)
urlpatterns = [
    # Путь для страницы со списком новостей
    path('', views.PostsList.as_view(), name='news_list'),
    # Путь для страницы с деталями новости
    path('<int:pk>/', views.PostsDetail.as_view(), name='news_detail'),
    path('search', views.PostsSearch.as_view(), name='new_search'),
    path('create/', views.PostsCreate.as_view(), name='news_create'),
    path('article/create/', views.PostsCreate.as_view(), name='article_create'),
    path('<int:pk>/edit/', views.PostsUpdate.as_view(), name='news_update'),
    path('article/<int:pk>/edit/', views.PostsUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', views.PostDelete.as_view(), name='news_delete'),
    path('article/<int:pk>/delete/', views.PostDelete.as_view(), name='article_delete')
]