from django.contrib import admin
from .models import *
from .models import MyModel, Category
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    model = Category

class MyModelAdmin(TranslationAdmin):
    model = MyModel

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(MyModel)