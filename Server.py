from WhereToBBTbot import WhereToBBT_bot
from getDistance import * 

update_id = None

#initialises the WhereToBBT_bot class
bot = WhereToBBT_bot("config.cfg")

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
            try:
                #extract out the text sent to bot
                message = item["message"]["text"]
            except:
                pass

            try:
                #extract out longitude and latitude
                longi = item["message"]["location"]["longitude"]
                lati = item["message"]["location"]["latitude"]
            except:
                pass

            from_ = item["message"]["from"]["id"]
            
            if message is not None:
                reply = make_reply(message)
                bot.send_message(reply, from_)
            else:
                bot.send_message("You longitude is " + str(longi), from_)
                bot.send_message("Your latitude is " + str(lati), from_)

    
