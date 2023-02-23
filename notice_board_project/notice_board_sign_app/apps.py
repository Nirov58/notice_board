from django.apps import AppConfig


class NoticeBoardSignAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notice_board_sign_app'

    def ready(self):
        from . import signals
