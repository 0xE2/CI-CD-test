#!/bin/env python3
# -*- coding: utf-8 -*-

import config
import telebot
import sqlite3
import hashlib


bot = telebot.TeleBot(config.token, threaded=False) #When threaded, sqlite doesn't work
test_chat_id = config.test_chat_id
bot_version = "0.01"
conn = sqlite3.connect('testers.db')
db = conn.cursor()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Bot started')
    print(message.chat.id)


@bot.message_handler(commands=["sub","subscribe"])
def subscribe(message):
    try:
        db.execute("INSERT INTO users VALUES (?, ?)", (message.chat.id, "tester"))
        db.connection.commit()
        bot.send_message(message.chat.id, 'You are successfully subscribed')
    except sqlite3.IntegrityError:
        bot.send_message(message.chat.id, 'You are already subscribed')


@bot.message_handler(commands=["unsub","unsubscribe"])
def unsubscribe(message):
    if(not "SELECT COUNT(*) FROM users WHERE telegram_id =:tg_id", {"tg_id" : message.chat.id}):
        bot.send_message(message.chat.id, 'You are not subscribed')
    else:
        db.execute("DELETE FROM users WHERE telegram_id =:tg_id", {"tg_id" : message.chat.id})
        db.connection.commit()
        bot.send_message(message.chat.id, 'You are successfully unsubscribed')


#@bot.message_handler(content_types=["text"])


def check_new_apk():
    try:
        with open("last_apk_hash") as f:
            old_hash = f.read()
    except FileNotFoundError:
        old_hash = "null"
    new_hash = get_file_hash("apk/app-debug.apk")   #If apk isn't delivered yet then bot just crashed
    if(old_hash != new_hash):
        with open("last_apk_hash", 'w') as f:
            f.write(new_hash)
        send_apk()


def get_file_hash(file):
    sha256h = hashlib.sha256()
    with open(file,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256h.update(byte_block)
        return sha256h.hexdigest()


def send_apk():
    db.execute("SELECT telegram_id FROM users WHERE rank == 'tester'")
    rows = db.fetchall()
    doc = open('apk/app-debug.apk', 'rb')
    for row in rows:
        bot.send_message(row[0], "New app version released:")
        bot.send_document(row[0], doc)
    doc.close()


if __name__ == '__main__':
    #bot.send_message(test_chat_id, "Bot version: " + bot_version)
    check_new_apk()
    bot.polling(none_stop=True)
