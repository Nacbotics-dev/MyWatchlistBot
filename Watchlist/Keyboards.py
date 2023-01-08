from telebot.types import *


def home_btn():
    keyboard = ReplyKeyboardMarkup(True)
    keyboard.row("🎬 My Watchlist","➕ New Watchlist")
    keyboard.row("👾 Report BUG 👾",)
    return(keyboard)

def report_bug_btn():
    keyboard = InlineKeyboardMarkup()
    report_bug = InlineKeyboardButton("👾 Report BUG 👾",url="https://forms.gle/XtvX4tLyJaxEd16r6")
    keyboard.add(report_bug)
    return(keyboard)


def Cancel_btn():
    keyboard = ReplyKeyboardMarkup(True)
    keyboard.row("❌ Cancel",)
    return(keyboard)


def watchlist_btn(movie):
    keyboard = InlineKeyboardMarkup()

    movie_id = hex(int(movie.movie_id.time_low))[2:]

    if movie.watched == True:
        text = "☑️ Unseen"
    else:
        text = "✅ Seen"

    toggle_btn = InlineKeyboardButton(text,callback_data=f"watched:{movie_id}")
    delete_btn = InlineKeyboardButton("🛑 Delete",callback_data=f"delete_movie:{movie_id}")
    
    keyboard.add(toggle_btn,delete_btn)
    return(keyboard)


