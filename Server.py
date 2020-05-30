from WhereToBBTbot import WhereToBBT_bot
from getDistance import * 
import csv
import pandas as pd
import telegram

update_id = None

#initialises the WhereToBBT_bot class
bot = WhereToBBT_bot("config.cfg")

#read CSV file

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
                #extract out the text sent to bot
                message = item["message"]["text"]
            except:
                pass

            try:
                #extract out longitude and latitude
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

            if message is not None:
                reply = make_reply("Please send me your location instead. To send your location, tap on the attachment button and choose 'Location'")
                bot.send_message(reply, from_)
            elif longi is not None and lati is not None :
                #bot.send_message("Your latitude is " + str(lati), from_)
                #bot.send_message("You longitude is " + str(longi), from_)
                for i in range(len(location_list)):
                    bot.send_message(str(i + 1) + ". " + location_list[i], from_)
            else:
                pass

    #location_keyboard = telegram.KeyboardButton(text = "Send current location", request _location = True)
    #custom_keyboard = [[location_keyboard]]
    #reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    #bot.send_message(chatid=chatid, text "Would you share your current location with me?", reply_markup = reply_markup)
