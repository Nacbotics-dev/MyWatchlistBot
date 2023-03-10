import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyWatchlist.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from apscheduler.schedulers.blocking import BlockingScheduler
import tzlocal
import time,telebot,json
from telebot.types import *
from django.db.models import Q
from ratelimiter import RateLimiter
from Watchlist.models import User,Watchlist
from django.shortcuts import render,redirect
from VeronicaNLP.web.Movies.TV import TVSHOWS
from django.views.decorators.http import require_http_methods
from VeronicaNLP.web.Movies.Tvshows4mobile import Tvshows4mobile
from apscheduler.schedulers.background import BackgroundScheduler



tv = TVSHOWS()
O2tv = Tvshows4mobile()
WEBHOOK_TOKEN = "1928565537:AAEUG6GAPoWZm3zcDuCkjal3kA-kgKCEbSA"
bot = telebot.TeleBot(WEBHOOK_TOKEN,parse_mode='HTML') #Telegram Bot API

sched = BlockingScheduler(timezone=str(tzlocal.get_localzone()))



def user_watchlists():
	users = [user.user_id for user in User.objects.all()]


	my_watchlist = []
	for user in users:
		watchlist = Watchlist.objects.filter(creator=user)
		if watchlist.exists():
			cmd = [tv.extract_movie_data(movie.movie_title,fztvseries=False)[0] for movie in watchlist]
			cmd = [movie['filename'] for movie in cmd]
			cmd = list(set(cmd))

			for title in cmd:
				movie = Watchlist.objects.filter(creator=user).filter(Q(movie_title__icontains=title)).last()
				my_watchlist.append(movie)
		else:
			pass

	return(my_watchlist)

def return_id(data,text):
	for id,j in enumerate(data):
		if text in j:
			return(id)
		else:
			pass

@sched.scheduled_job('interval', minutes=10)
def new_episode_notfication():
	movies = user_watchlists()

	for movie in movies:
		cmd = tv.extract_movie_data(movie.movie_title,fztvseries=False)[0]
		print(f"Currently handling {cmd['filename']}")
		missed_episodes = O2tv.return_missed_episodes(cmd)

		if type(missed_episodes) is str:
			bot.send_message(movie.creator.chat_id,missed_episodes)
		else:
			try:
				last_episode_id = return_id(missed_episodes,cmd["episode"])
				#[id for (id,j) in enumerate(missed_episodes) if j == cmd["episode"]][0]
				if movie.available ==True:
					pass
				else:
					movie.available=True
					movie.save()

					#SEND UPDATE OF NEW EPISODES
					my_movie = f"<b>{cmd['filename']} - {cmd['format']} is out for download</b>"
					bot.send_message(movie.creator.chat_id,my_movie)

				try:
					for episode in missed_episodes[last_episode_id+1:]:
						Watchlist(movie_title=f"{cmd['filename']} {cmd['season']} {episode}",creator=movie.creator,available=True).save()
						
						cmd = tv.extract_movie_data(f"{cmd['filename']} {cmd['season']} {episode}",fztvseries=False)[0]
						
						my_movie = f"<b>{cmd['filename']} - {cmd['format']} is out for download</b>"
						bot.send_message(movie.creator.chat_id,my_movie)
				except Exception as e:
					print(str(e),"New Episode Notification Error")

			except IndexError:
				pass

sched.start()


# def start():
# 	scheduler = BackgroundScheduler(timezone="UTC",daemon=True)
# 	scheduler.add_job(new_episode_notfication, 'cron', hour=5)
# 	scheduler.start()