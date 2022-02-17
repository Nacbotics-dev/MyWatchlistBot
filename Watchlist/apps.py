from django.apps import AppConfig


class WatchlistConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'Watchlist'

	# def ready(self):
	# 	from .views import start
	# 	start()

