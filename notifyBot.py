import os
import discord
import Anilist
import keep_alive
from time import sleep
from discord.ext import commands,tasks


bot = commands.Bot(command_prefix='.')
user = Anilist.Anilist('<Anilist username>')

channel_id = 827178386132172840 #channel id to send msg in

#creates two process one for comands and another for tasks

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

    @bot.command(brief="List the anime to be Aired this week")
    async def list(ctx):
        l = user.getWatchingList()
        for i in l:
            embed = discord.Embed(title=i['title'],url=i['url'],description=f"Episode: {i['epiNo']} (yet to be aired)")
            embed.set_image(url=i['img'])
            await ctx.send(embed=embed)

else:
    #runs the "announce" function once a week
    @tasks.loop(seconds=604800)
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
bot.run("<client_secret>")
