from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    # this method is called whem this app is ready
    def ready(self) -> None:
        import store.signals
