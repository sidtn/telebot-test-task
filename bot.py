import telebot
from telebot import types
from settings import *
from db_manager import DBManager


base = DBManager(DB_NAME, DB_USER, PASSWORD)
base.create_tables()
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	if not base.check_user(message.from_user.id):
		base.add_user(message.from_user.id)
	markup = types.InlineKeyboardMarkup()
	key1 = types.InlineKeyboardButton("Профиль", callback_data='__profile')
	key2 = types.InlineKeyboardButton("Статистика", callback_data='__stats')
	markup.add(key1, key2)
	bot.send_message(message.chat.id, text='hi', reply_markup=markup)


@bot.callback_query_handler(lambda call: call.data == '__profile')
def show_profile(call):
	message = f'first name - {call.from_user.first_name} \n'\
			f'last name - {call.from_user.last_name} \n'\
			f'username - {call.from_user.username} \n'\
			f'user id - {call.from_user.id} \n'
	bot.send_message(call.message.chat.id, message)


@bot.callback_query_handler(lambda call: call.data == '__stats')
def show_stat(call):
	num_of_users = base.get_user_quantity()[0][0]
	bot.send_message(call.message.chat.id, f'Number of users - {num_of_users}')


@bot.message_handler(func=lambda message: True)
def answer_to_message(message):
	last = base.read_last_message()
	first = message.text.split()[0]
	base.add_message(message.from_user.id, message.text.split()[-1])
	if last:
		bot.reply_to(message, f'{first}\n{last[0]}')
	else:
		bot.reply_to(message, f'{first}\nno last message')


if __name__ == '__main__':
	bot.infinity_polling()
