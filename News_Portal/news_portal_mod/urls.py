from django.urls import path
from . import views

urlpatterns = [
    # Путь для страницы со списком новостей
    path('news/', views.PostsList.as_view(), name='news_list'),
    # Путь для страницы с деталями новости
    path('news/<int:pk>/', views.PostsDetail.as_view(), name='news_detail'),
]