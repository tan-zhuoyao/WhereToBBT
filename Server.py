from WhereToBBTbot import WhereToBBT_bot

update_id = None

#initialises the WhereToBBT_bot class
bot = WhereToBBT_bot("config.cfg")

def make_reply(msg):
    if msg is not None:
        reply = "Okay"
    return reply

while True:
    print("...")
    updates = bot.get_updates(offset=update_id)
    updates = updates["resut"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = item["message"]["text"]
            except:
                message = None
            from_ = item["message"]["text"]["id"]
            reply = make_reply(message)
            bot.send_message(reply, from_)
    
