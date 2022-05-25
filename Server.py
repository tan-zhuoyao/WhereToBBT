from WhereToBBTbot import WhereToBBT_bot
from getDistance import *
import pandas as pd
import telegram

update_id = None

# initialises the WhereToBBT_bot class
bot = WhereToBBT_bot("config.cfg")

# read CSV file
bbt_locations = pd.read_csv('BBTgeocodes.csv')

filter_list = []
filter_dict = {}


def make_reply(msg):
    if msg is not None:
        reply = msg
    return reply


bot.send_message("no", -1001334729910)

while True:
    print("...")
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]

    if updates:
        for item in updates:
            print(item)
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
            except:
                pass

            try:
                from_ = item["message"]["from"]["id"]
            except:
                from_ = item["edited_message"]["from"]["id"]

            try:
                username = item["message"]["from"]["username"]
            except:
                username = "unknown"

            print(username)

            if from_ in filter_dict.keys() and lati is not None and longi is not None:
                brand = filter_dict.pop(from_)
                location_list = getTopBrand(
                    lati, longi, bbt_locations, 3, brand)
                for i in range(len(location_list)):
                    bot.bot.sendMessage(chat_id=from_, text=str(
                        i + 1) + ". " + location_list[i])
                start_keyboard = telegram.KeyboardButton(text="return")
                custom_keyboard = [[start_keyboard]]
                reply_markup = telegram.ReplyKeyboardMarkup(
                    keyboard=custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
                bot.bot.sendMessage(
                    chat_id=from_, text="Return to main menu", reply_markup=reply_markup)

            elif message == "/start" or message == "return":
                # trigger a button to send location
                location_keyboard = telegram.KeyboardButton(
                    text="Find me BBT!🍵", request_location=True)
                brand_keyboard = telegram.KeyboardButton(
                    text="Filter by brand!")
                custom_keyboard = [[location_keyboard], [brand_keyboard]]
                reply_markup = telegram.ReplyKeyboardMarkup(
                    keyboard=custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
                bot.bot.sendMessage(
                    chat_id=from_, text="Welcome to WhereToBBT!", reply_markup=reply_markup)

            elif message == "Filter by brand!":
                # list brands
                filter_list.append(from_)
                koi_keyboard = telegram.KeyboardButton(text="Koi")
                gongcha_keyboard = telegram.KeyboardButton(text="Gong Cha")
                liho_keyboard = telegram.KeyboardButton(text="LiHo")
                playmade_keyboard = telegram.KeyboardButton(text="Playmade")
                heytea_keyboard = telegram.KeyboardButton(text="HeyTea")
                tigersugar_keyboard = telegram.KeyboardButton(
                    text="Tiger Sugar")
                rnb_keyboard = telegram.KeyboardButton(text="R&B Tea")
                xingfutang_keyboard = telegram.KeyboardButton(
                    text="Xing Fu Tang")
                partea_keyboard = telegram.KeyboardButton(text="PARTEA")
                teatreecafe_keyboard = telegram.KeyboardButton(
                    text="Tea Tree Cafe")
                brands_keyboard = [[gongcha_keyboard], [koi_keyboard], [liho_keyboard], [playmade_keyboard], [
                    rnb_keyboard], [teatreecafe_keyboard], [tigersugar_keyboard], [xingfutang_keyboard]]
                reply_markup = telegram.ReplyKeyboardMarkup(
                    keyboard=brands_keyboard, resize_keyboard=True, one_time_keyboard=True)
                bot.bot.sendMessage(
                    chat_id=from_, text="Choose your brand!", reply_markup=reply_markup)

            elif message is not None and from_ in filter_list:
                filter_list.remove(from_)
                filter_dict[from_] = message
                location_keyboard = telegram.KeyboardButton(
                    text="BBT me now!", request_location=True)
                custom_keyboard = [[location_keyboard]]
                reply_markup = telegram.ReplyKeyboardMarkup(
                    keyboard=custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
                bot.bot.sendMessage(
                    chat_id=from_, text="Send your location", reply_markup=reply_markup)

            # net to catch random messages
            elif message is not None:
                # prompts user to /search
                reply = make_reply("Please enter '/start' to start search")
                bot.send_message(reply, from_)

            # user clicks find me bubble tea
            elif longi is not None and lati is not None:
                location_list = getTopKClosest(lati, longi, bbt_locations, 3)
                for i in range(len(location_list)):
                    bot.bot.sendMessage(chat_id=from_, text=str(
                        i + 1) + ". " + location_list[i])
            else:
                pass
