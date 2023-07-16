from tgtg import TgtgClient
import discord
from discord.ext import commands
import credentials 
from credentials import too_good_to_go_credentials, discord_token


TGTG_CLIENT = TgtgClient(access_token=too_good_to_go_credentials["access_token"], 
                    refresh_token=too_good_to_go_credentials["refresh_token"],
                    user_id=too_good_to_go_credentials["user_id"],
                    cookie=too_good_to_go_credentials["cookie"])

DISC_TOKEN = discord_token["token"]

def make_request(client):
    items = client.get_items()
    found_goodies = []
    for item in items:
        if item["items_available"] > 0:
            print(f'{item["display_name"]} has {item["items_available"]} goodie bags to pick up!')
            found_goodies.append({"place": item["display_name"], "items_available": item["items_available"]})
    return found_goodies  


def send_message_to_discord(goodies):
    intents = discord.Intents.default()
    intents.message_content = True

    discord_client = discord.Client(intents=intents)
    bot = commands.Bot(command_prefix='!', intents=intents)


    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        for guild in bot.guilds:
            channel = guild.system_channel #getting system channel
            if channel.permissions_for(guild.me).send_messages: #making sure you have permissions
                await channel.send(str(goodies))
        await bot.close()   

    bot.run(DISC_TOKEN)


if __name__ ==  '__main__':
    # get available stuff from favourites
    goodies = make_request(TGTG_CLIENT)

    # send message to discord
    send_message_to_discord(goodies)
    