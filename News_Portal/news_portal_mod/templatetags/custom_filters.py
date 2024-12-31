from django import template
register = template.Library()
BAD_WORDS = ['']
@register.filter()
def censor(value):
   if not value:
       return value
   for word in BAD_WORDS:
       value = value.replace(word, '*' * len(word))
   return value