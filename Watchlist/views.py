from .messages import *
from .Keyboards import *
import time,telebot,json
from telebot.types import *
from django.db.models import Q
from .models import User,Watchlist
from ratelimiter import RateLimiter
from django.http import HttpResponse
from django.shortcuts import render,redirect
from VeronicaNLP.web.Movies.TV import TVSHOWS
from MyWatchlist.settings import WEBHOOK_URL,WEBHOOK_TOKEN
from django.views.decorators.http import require_http_methods
from VeronicaNLP.web.Movies.Tvshows4mobile import Tvshows4mobile
from apscheduler.schedulers.background import BackgroundScheduler



tv = TVSHOWS()
O2tv = Tvshows4mobile()

bot = telebot.TeleBot(WEBHOOK_TOKEN,parse_mode='HTML') #Telegram Bot API
bot.enable_save_next_step_handlers(filename="handlers-saves/step.save",delay=2)


def user_details(message):
	detail = {}
	detail["chat_id"] = message.chat.id
	detail["msg_type"] = message.chat.type
	detail["user_id"] = message.from_user.id
	detail["username"] = message.from_user.username
	return(detail)


# CALLBACK QUERY HANDLING OCCURS HERE

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

	try:
		userID = call.from_user.id
		chat_id = call.message.chat.id
		user = User.objects.get(user_id=userID)

		if call.data.startswith("watched:"):
			q = call.data.split(":")[1]
			movie = Watchlist.objects.filter(Q(movie_id__icontains=q)).first()

			if movie.watched == True:
				Watchlist.objects.filter(movie_id = movie.movie_id).update(watched=False)
			else:
				Watchlist.objects.filter(movie_id = movie.movie_id).update(watched=True)  


			movie_data = tv.extract_movie_data(movie.movie_title)[0]

			movie = Watchlist.objects.get(movie_id = movie.movie_id)

			if movie.available == True:
				flag = "✅"
			else:
				flag = "☑️"

			if movie.watched == True:
				my_movie = f"<s>{movie_data['filename']} - {movie_data['format']} {flag} *</s>"
			else:
				my_movie = f"{movie_data['filename']} - {movie_data['format']} {flag} *"

			bot.answer_callback_query(call.id, "status has changed")
			bot.edit_message_text(chat_id=chat_id, text=my_movie, message_id=call.message.message_id,reply_markup=watchlist_btn(movie))

		elif call.data.startswith("delete_movie:"):
			q = call.data.split(":")[1]
			Watchlist.objects.filter(Q(movie_id__icontains=q)).first().delete()
			bot.answer_callback_query(call.id, "movie has been removed")
			bot.delete_message(chat_id=chat_id,message_id=call.message.message_id)
		else:
			pass
	except Exception as e:
		print(f"CALLBACK ERROR : {e}")
		pass


def get_movie_name(message):
	user_detail = user_details(message)
	if message.text != "":
		if message.text == "❌ Cancel" or message.text == "/cancel":
			bot.clear_step_handler_by_chat_id(chat_id=user_detail["chat_id"])
			bot.send_message(user_detail["chat_id"],"Action terminated",reply_markup=home_btn())
		else:
			movie_data = tv.extract_movie_data(message.text)
			if type(movie_data) is not str:
				user = User.objects.get(user_id=user_detail["user_id"])
				watchlist = Watchlist(movie_title=message.text,creator=user)
				watchlist.save()

				movie_data = movie_data[0]
				my_movie = f"{movie_data['filename']} - {movie_data['format']}"

				bot.send_message(user_detail["chat_id"],f"{my_movie} has been added to your watchlist",reply_markup=home_btn())
			else:
				msgs = bot.send_message(user_detail["chat_id"],movie_data)
				bot.register_next_step_handler(msgs,get_movie_name)
	else:
		pass


@bot.message_handler(commands=['start'])
def start(message):
	user_detail = user_details(message)

	if user_detail["msg_type"] == "private":
		try:
			user = User.objects.get(user_id=user_detail["user_id"])
		except User.DoesNotExist:
			user = User(user_name=user_detail["username"],chat_id=user_detail["chat_id"],user_id=user_detail["user_id"])
			user.save()

		msg = menu_text.format(user_detail["username"])
		bot.send_message(user_detail["chat_id"],msg,reply_markup=home_btn())
	else:
		pass


@bot.message_handler(commands=['cancel'])
def cancel(message):
	user_detail = user_details(message)
	if user_detail["msg_type"] == "private":
		bot.clear_step_handler_by_chat_id(chat_id=user_detail["chat_id"])
		bot.send_message(user_detail["chat_id"],"Action terminated",reply_markup=home_btn())
	else:
		pass


@bot.message_handler(commands=['new_watchlist'])
def new_watchlist(message):
	user_detail = user_details(message)

	if user_detail["msg_type"] == "private":
		msgs = bot.send_message(user_detail["chat_id"],"Enter the <b>Title</b>, <b>Season</b> and <b>episode</b> of the movie",reply_markup=Cancel_btn())
		bot.register_next_step_handler(msgs,get_movie_name)
	else:
		pass


@bot.message_handler(commands=['view_watchlist'])
def view_watchlist(message):
	user_detail = user_details(message)

	if user_detail["msg_type"] == "private":
		my_watchlist = Watchlist.objects.filter(creator=user_detail['user_id'])

		if my_watchlist.exists():
			for movie in my_watchlist:
				movie_data = tv.extract_movie_data(movie.movie_title)[0]

				if movie.available == True:
					flag = "✅"
				else:
					flag = "☑️"

				if movie.watched == True:
					my_movie = f"<s>{movie_data['filename']} - {movie_data['format']} {flag}</s>"
				else:
					my_movie = f"{movie_data['filename']} - {movie_data['format']} {flag}"
				bot.send_message(user_detail['chat_id'],my_movie,reply_markup=watchlist_btn(movie))
		else:
			bot.send_message(user_detail["chat_id"],"You currently do not any watchlist",reply_markup=home_btn())

	else:
		pass


@bot.message_handler(content_types=['text'])
def reply_msg(message):
	user_detail = user_details(message)
	
	if user_detail["msg_type"] == "private":

		if message.text == "🎬 My Watchlist":
			view_watchlist(message)
		elif message.text == "➕ New Watchlist":
			new_watchlist(message)

		elif message.text == "👾 Report BUG 👾":
			msg = "Hey are u experiencing difficulty? \nyou can report it and we will fix it ASAP"
			bot.send_message(user_detail['chat_id'],msg,reply_markup=report_bug_btn())
		else:
			pass


	else:
		pass


@require_http_methods(["GET","POST"])
@RateLimiter(max_calls=100, period=1)
def WebConnect(request):
	# Listens only for GET and POST requests
	# returns django.http.HttpResponseNotAllowed for other requests
	# Handle the event appropriately

	if request.method == 'POST':
		jsondata = request.body
		data = json.loads(jsondata)
		update = telebot.types.Update.de_json(data)
		bot.process_new_updates([update])
		return HttpResponse(status=201)
	else:
		bot.remove_webhook()
		bot.set_webhook(url=WEBHOOK_URL+WEBHOOK_TOKEN)
		return HttpResponse(status=201)


bot.load_next_step_handlers(filename="handlers-saves/step.save")
