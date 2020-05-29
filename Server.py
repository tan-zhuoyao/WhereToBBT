from WhereToBBTbot import WhereToBBT_bot

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
            try:
                #extract out the text sent to bot
                message = item["message"]["text"]
                print(message)
            except:
                #if error then just return default text
                message = "I did not get you there. Sorry."
            try:
                #extract out longitude and latitude
                longi = item["message"]["location"]["longitude"]
                lati = item["message"]["location"]["latitude"]
            except:
                longi = 0
                lati = 0
            
            from_ = item["message"]["from"]["id"]
            reply = make_reply(message)
            #bot.send_message(reply, from_)
            bot.send_message("You longitude is " + str(longi), from_)
            bot.send_message("Your latitude is " + str(lati), from_)
    
