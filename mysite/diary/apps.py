from django.apps import AppConfig


class DiaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # ЗДЕСЬ ДОЛЖНО БЫТЬ СТРОГО 'diary', А НЕ 'servant'
    name = 'diary'

class ServanConfig(AppConfig):
    name = 'servant'
