from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = "notifications"

    def ready(self):
        # Import signals here so they are registered exactly once when the app is ready.
        # Avoid importing signals at module level from other places.
        try:
            import notifications.signals  # noqa: F401
        except Exception:
            # Let Django surface the error during startup if there is one
            raise
