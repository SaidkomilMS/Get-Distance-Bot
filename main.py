from telegram import *
from telegram.ext import *
from dbworking import *
from config import *

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

loc_num = {}
last_location = {}

def start(update, context):
	global loc_num
	chat_id = update.effective_chat.id
	if is_not_in_db(chat_id): add_user(chat_id)
	user = update.message.from_user
	context.bot.send_message(chat_id=496583471, text=f'The user <b>{user.first_name}</b> has started me!\nThe username: @{user.username}\nThe userID: {chat_id}', parse_mode=ParseMode.HTML)
	loc_num[chat_id] = 1
	keyboard = [[KeyboardButton("Отправить моё местоположение", request_location=True)]]
	reply_markup = ReplyKeyboardMarkup(keyboard)
	context.bot.send_message(chat_id=chat_id, text="<strong>Добро пожаловать!</strong>\n\nОтправьте два местоположения и я определю расстояние между ними\nОтправьте трансляцию (live) и я определю сколько вы продвинулись.\n\n<em>P. S. Я не храню данные о вашем местоположении</em>", parse_mode=ParseMode.HTML, reply_markup=reply_markup)

def location(update, context):
	global last_location, loc_num
	chat_id = update.effective_chat.id
#	context.bot.send_message(chat_id, text=f'Update:\n{str(update)}')
	if update.message:
		if update.message.location:
		#	context.bot.send_message(chat_id, text=f'Update.message.location:\n{str(update.message.location)}')
			if loc_num[chat_id] == 1:
				last_location[chat_id] = update.message.location
				save_loc(chat_id, last_location[chat_id])
				loc_num[chat_id] = 2
				set_loc_num(chat_id, 2)
				context.bot.send_message(chat_id, text="А теперь отправьте второе местоположение")
			else:
				distance = get_distance(update.message.location, chat_id, last_location)
				loc_num[chat_id] = 1
				set_loc_num(chat_id, 1)
				distance, race, n unit, suffix = distance_handler(distance)
				context.bot.send_message(chat_id, text=f"Расстояние между местоположениями: {distance:.{n}f} {unit}{suffix}\nПо дороге будет примерно: ~{race:.{n}f} {unit}{suffix}")
	elif update.edited_message:
		loc_num[chat_id] = 1
		set_loc_num(chat_id, 1)
		distance = get_distance(update.edited_message.location, chat_id)
		distance, race, n unit, suffix = distance_handler(distance)
		context.bot.send_message(chat_id, text=f"Вы прошли {distance:.{n}f} {unit}{suffix}")

def main():
	global loc_num
	updater = Updater(
		TOKEN,
		use_context = True)
	dp = updater.dispatcher
	
	loc_handler = MessageHandler(Filters.location, location)
	start_handler = CommandHandler('start', start)
	
	dp.add_handler(loc_handler)
	dp.add_handler(start_handler)
	
	loc_num = get_loc_nums()
	last_loc = get_last_locs()
	
	print("Bot is working...")
	updater.start_polling()
	updater.idle()
	
if __name__ == '__main__':
	main()