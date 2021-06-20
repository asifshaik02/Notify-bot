import os
import discord
import Anilist
import keep_alive
from time import sleep
from discord.ext import commands,tasks


# Add anilist user name and discord client secret
username = None
secret = None

# format time
intervals = (
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)

def display_time(seconds, granularity=3):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

user = Anilist.Anilist(username)

bot = commands.Bot(command_prefix='.')

channel_id = None # channel id to send msg in


# creates two process one for comands and another for tasks
if os.fork():
    @bot.event
    async def on_ready():
        print("Bot is online")

    #commands
    @bot.command(brief="Returns ping of the bot")
    async def ping(ctx):
        await ctx.send(f'Pong! {round (bot.latency * 1000)}ms ')

    @bot.command(brief="Stops bot from running")
    async def stop(ctx):
        await bot.close()
    
    @bot.command(brief="Clear messages. Takes args of number of msg to delete")
    async def clear(ctx,n=5):
        n = n + 1
        await ctx.channel.purge(limit=n)
    
    @bot.command(brief="change user.requires new username as an argument")
    async def register(ctx,uname):
        username = uname

    @bot.command(brief="List airing schedules for anime in your watch list")
    async def list(ctx):
        l = user.getWatchingList()
        embed = discord.Embed(
            title="Airing Schedule",
            description="Your watchlist airing schedule"
        )
        for i in l:
          embed.add_field(
              name=i['title'],
              value=f"Episode: [{i['epiNo']}]({i['url']}) \nTime: {display_time(i['timeRem'])}",
              inline=False)

        await ctx.send(embed=embed)

else:
    #runs the "announce" function once a day
    @tasks.loop(seconds=86400)
    async def announce():
        channel = bot.get_channel(channel_id)
        list = user.getWatchingList()
        print(list)

        while (len(list) != 0):
            d = list.pop()
            sleep(d['timeRem'])

            for i in list:
                i['timeRem'] -= d['timeRem']

            embed = discord.Embed(title=d['title'],url=d['url'],description=f"Episode: {d['epiNo']}")
            embed.set_image(url=d['img'])
            await channel.send(embed=embed)

    #wait till the bot is ready
    @announce.before_loop
    async def before_printer():
        print('waiting...')
        await bot.wait_until_ready()

    #start the task
    announce.start()

#start server
keep_alive.keep_alive()

#run Bot
bot.run(secret)
