from django import forms
from .models import Post, Category
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'title_post',
           'text_post',
       ]

   def clean(self):
       cleaned_data = super().clean()
       text_post = cleaned_data.get("text_post")
       title_post = cleaned_data.get("title_post")

       if title_post == text_post:
           raise ValidationError(
               "Описание не должно быть идентично названию."
           )
       if len(text_post) < 20:
           raise ValidationError("Тескт поста должен содержать минимум 20 символов.")

       return cleaned_data

class SubscribersForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.HiddenInput())
