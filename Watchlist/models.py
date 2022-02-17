import uuid
from django.db import models
from django.urls import reverse
from datetime import datetime




class User(models.Model):
	"""
		The model holding all our telegram users
	"""
	chat_id = models.CharField(max_length=120,null=True,blank=False)
	user_name = models.CharField(max_length=120,null=True,blank=True,editable=False)
	user_id = models.CharField(primary_key=True,max_length=120, null=False, blank=False,editable=False)
	date_joined = models.DateTimeField(auto_now_add=True,null=False,editable=False)#date user started using the bot
	def __str__(self):
		return(str(self.user_id))


class Watchlist(models.Model):
	"""
		The model holding all movies in watchlist
	"""	
	
	movie_id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False, unique=True) # A unique i dentifier of the watchlist
	creator = models.ForeignKey(User, on_delete=models.CASCADE,editable=False) # The creator of this watchlist
	movie_title = models.CharField(max_length=120,blank=False,null=False) # The movie title this could be a series or just a movie
	watched = models.BooleanField(default=False) # This is used to mark a movie as watched or not
	available = models.BooleanField(default=False) # This is used to mark a movie ass available for download
	date_added = models.DateTimeField(auto_now_add=True,null=False,editable=False)#date the movie was added


	def __str__(self):
		return(str(self.movie_id))

	class Meta:
		ordering = ('date_added',)

