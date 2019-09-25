# _*_ coding: utf-8 _*_

import config
import telebot

bot = telebot.TeleBot(config.token)
dev_chat = config.test_chat_id
bot_version = "0.01"

@bot.message_handler(commands=["start"])
def start(message):
	bot.send_message(message.chat.id, "Bot started")

if __name__ == '__main__':
	bot.send_message(dev_chat, "Bot version: " + bot_version)
	bot.polling(none_stop=True)
