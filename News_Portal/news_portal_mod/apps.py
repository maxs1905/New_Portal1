from django.apps import AppConfig
class NewsPortalModConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_portal_mod'
    def ready(self):
        import news_portal_mod.signals







