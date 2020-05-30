from WhereToBBTbot import WhereToBBT_bot
from getDistance import * 
import csv
import pandas as pd
import telegram

update_id = None

# initialises the WhereToBBT_bot class
bot = WhereToBBT_bot("config.cfg")

# read CSV file

bbt_locations = pd.read_csv('BBTgeocodes.csv')

def make_reply(msg):
    if msg is not None:
        reply = msg
    return reply

while True:
    print("...")
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]

    if updates:
        for item in updates:
            update_id = item["update_id"]
            message = None
            longi = None
            lati = None
            location_list = []

            try:
                # extract out the text sent to bot
                message = item["message"]["text"]
            except:
                pass

            try:
                # extract out longitude and latitude
                longi = item["message"]["location"]["longitude"]
                lati = item["message"]["location"]["latitude"]
                location_list =  getTopKClosest(lati, longi, bbt_locations, 3)
                print(location_list)
            except:
                pass

            try:
                from_ = item["message"]["from"]["id"]
            except:
                from_ = item["edited_message"]["from"]["id"]

            if message == "/start":
                # trigger a button to send location
                location_keyboard = telegram.KeyboardButton(text="Find me BBT!🍵", request_location=True)
                brand_keyboard = telegram.KeyboardButton(text="Filter by brand!")
                custom_keyboard = [[location_keyboard],[brand_keyboard]]
                reply_markup = telegram.ReplyKeyboardMarkup(keyboard=custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
                bot.bot.send_message(chat_id=from_, text="Welcome to WhereToBBT!", reply_markup=reply_markup)
            elif message == "Filter by brand!":
                # list brands
                koi_keyboard = telegram.KeyboardButton(text="Koi")
                gongcha_keyboard = telegram.KeyboardButton(text="Gongcha")
                liho_keyboard = telegram.KeyboardButton(text="Liho")
                brands_keyboard = [[koi_keyboard],[gongcha_keyboard],[liho_keyboard]]
                reply_markup = telegram.ReplyKeyboardMarkup(keyboard=brands_keyboard, resize_keyboard=True, one_time_keyboard=True)
                bot.bot.send_message(chat_id=from_, text="Choose your brand!", reply_markup=reply_markup)
            elif message is not None:
                # prompts user to /search
                reply = make_reply("Please enter '/start' to start search")
                bot.send_message(reply, from_)
            elif longi is not None and lati is not None :
                for i in range(len(location_list)):
                    bot.bot.sendMessage(chat_id=from_, text=str(i + 1) + ". " + location_list[i])
            else:
                pass

