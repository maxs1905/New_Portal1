from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.core.cache import cache
class Author (models.Model):
    rating = models.IntegerField(default = 0)
    name_author = models.OneToOneField(User, on_delete = models.CASCADE)

    def update_rating(self):
        post_rating = sum([post.rating_post * 3 for post in self.posts.all()])
        comments_rating = sum([comment.rating_comment for comment in self.name_author.comment_set.all()])
        post_comment_rating = sum([comment.rating_comment for post in self.posts.all() for comment in post.comment_set.all()])
        self.rating = post_rating + comments_rating + post_comment_rating
        self.save()
    def __str__(self):
        return self.name_author.username



class Category (models.Model):
    name_category = models.CharField(max_length=255, unique= True)
    subscribers = models.ManyToManyField(User, related_name='subscribers_categories')

    def __str__(self):
        return self.name_category

class Post (models.Model):
    POST_TYPES = [
        ('Article', 'Статья'),
        ('News', 'Новости'),
    ]
    author = models.ForeignKey(Author,on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=7, choices= POST_TYPES)
    create_time = models.DateTimeField(auto_now_add=True)
    category_post = models.ManyToManyField(Category, through='PostCategory')
    title_post = models.CharField(max_length=255)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)

    def preview(self):
        return self.text_post[:124] + '...' if len(self.text_post) > 124 else self.text_post
    def like (self):
        self.rating_post += 1
        self.save()
    def dislike (self):
        self.rating_post -= 1
        self.save()

    def __str__(self):
        return f'{self.title_post.title()}'

    def get_absolute_url(self):

        return reverse('news_detail', kwargs={'pk':self.pk})

    def clean(self):
        today = datetime.now().date()
        post_today = Post.objects.filter(author=self.author, create_time__date=today)
        if post_today.count() >= 3:
            raise ValidationError('Вы не можете побликовать более 3 постов в день.')

    def get_absolute_url(self):
        return f'/news/{self.id}'
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')



class PostCategory (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment (models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    create_time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()


