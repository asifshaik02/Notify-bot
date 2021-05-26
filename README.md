# Notify-bot
A Discord bot to notify when a new Episode of an anime in my watchlist is aired.<br>
we use anilist's graphql api to obtain data and discord's bot to send notification to server.<br><br>
<b>Note:</b> you should have an account in [anilist](https://anilist.co/) and [Discord](https://discord.com/)<br>

# Setup
```console
$ git clone https://github.com/asifshaik02/Notify-bot.git 
$ cd Notify-bot 
$ pip install requirements.txt
```
* open [notifyBot.py](/notifyBot.py) add your <b>anilist username</b> and <b>discord bot client_secret</b>
* To get  discord's client_secret goto [Discord's developer dashboard](https://discord.com/developers/applications) 
* create an application. [refer here](https://realpython.com/how-to-make-a-discord-bot-python/)

# Documentation References
* [Anilist Graphql Api](https://anilist.gitbook.io/anilist-apiv2-docs/)
* [Graphql](https://graphql.org/learn/queries/)
* [Discord Documentation](https://discordpy.readthedocs.io/en/latest/index.html)

## Hosting(optional)
I used [repel.it](https://replit.com/) to host my bot.
Refer [here](https://replit.com/talk/learn/Hosting-discordpy-bots-with-replit/11008) to keep the bot running 24/7
