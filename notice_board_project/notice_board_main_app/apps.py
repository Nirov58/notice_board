from django.apps import AppConfig


class NoticeBoardMainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notice_board_main_app'

    def ready(self):
        from . import signals
