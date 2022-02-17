from django.contrib import admin
from .models import User,Watchlist




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	search_fields = ('user_id','user_name',)
	list_display = ['user_id','user_name','date_joined',]



@admin.register(Watchlist)
class UserAdmin(admin.ModelAdmin):
	search_fields = ('movie_id','movie_title','creator','creator__user_name',)
	list_display = ['movie_id','movie_title','creator','available','date_added']
