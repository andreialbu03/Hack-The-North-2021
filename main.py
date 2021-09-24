from game import gameplayinstance
import discord
import news
import game
import info
import user_db
import questions
import tips
import help
import os
from dotenv import load_dotenv, find_dotenv
import ISO3166


client = discord.Client()
load_dotenv(find_dotenv())
TOKEN=os.environ.get("TOKEN")

@client.event
async def on_ready():
    print('We have logged in a {0.user}'.format(client))
    return


def prettify_num(num):
    counter = 0
    res = ""
    for i in range(1, len(num)+1):
        res = num[-i] + res
        counter += 1
        if counter % 3 == 0:
            res = "," + res
    if counter >= 3 and res[0] == ",":
        res = res[1:]
    return res
        

async def display_covid_stats(command, covid_stats, country):
    if command == 'covid_country':
        output = discord.Embed(
            title = f':flag_{ISO3166.ISO3166rev.get(country).lower()}: Covid Statistics for {country.capitalize()} :flag_{ISO3166.ISO3166rev.get(country).lower()}:',        
            color = 0xb23831
        )
        
        info_display = ''

        for key, value in covid_stats.items():
            value = prettify_num(str(value))
            if key == 'cases':
                info_display += f'Total Cases: {value}\n'
                continue
            info_display += f'{key.capitalize()}: {value}\n'

        output.add_field(name='Statistics:', value=info_display)
        
        return output
    
    elif command == 'covid_global':
        output = discord.Embed(
            title = '🌎Global Covid-19 Statistics🌎',
            color = 0xb23831
        )

        info_display = ''

        for key, value in covid_stats.items():
            value = prettify_num(str(value))
            if key == 'cases':
                info_display += f'Total Cases: {value}\n'
                continue
            info_display += f'{key.capitalize()}: {value}\n'

        output.add_field(name='Statistics:', value=info_display)
        
        return output


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content).lower()
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    # first index is the command, second is the param
    formattedlist = user_message.split(" ") #first index is the command, second is the param
    # help command (please list all commands with brief description)
    if formattedlist[0] == '~help':
        await message.channel.send(embed=help.get_help())

    # global covid stats
    if formattedlist[0] == '~covid-global':
        stats, url_valid = info.covid_total()
        if url_valid:
            await message.channel.send(embed = await display_covid_stats('covid_global', stats, None))
        else:
            await message.channel.send('Country name is invalid')

    # covid stats (region specific) 
    # command: ~covid param(country name)
    if formattedlist[0] == '~covid':
        stats, url_valid = info.covid_country("".join(formattedlist[1:]))
        if url_valid:
            await message.channel.send(embed = await display_covid_stats('covid_country', stats, "".join(formattedlist[1:])))
        else:
            await message.channel.send('Country name is invalid')

    # covid news (region specific)
    if formattedlist[0] == '~covid-news':
        if(len(formattedlist) == 2):
            await message.channel.send(embed = await news.get_covid_news_location(formattedlist[1]))
            return
        else:
            await message.channel.send(embed = await news.get_covid_news())
            return

    # set region
    if formattedlist[0] == '~set-region':
        pass

    # display tips to stay safe from covid
    if formattedlist[0] == '~tips':
        await message.channel.send(tips.get_tips())
        return

    if formattedlist[0] == '~game':
        if message.author in user_db.usergameinstance:
            await message.channel.send(embed = discord.Embed(title = "Ongoing Game", description="Use ~answer {a/A or b/B} to respond to a question.\nEnter ~game to see your question again",color = 0xb23831).add_field(name="Current Question: ", value=f'{questions.questions[user_db.usergameinstance[message.author].qindex][0]}'))
            return
        else:
            user_db.usergameinstance[message.author] = gameplayinstance()
            await message.channel.send(embed = await user_db.usergameinstance[message.author].iterate("", message.author))
            return

    if formattedlist[0] == '~answer':
        if not message.author in user_db.usergameinstance:
            await message.channel.send("Start a game with ~game")
            return
        if len(formattedlist) == 2:
            await message.channel.send(embed = await user_db.usergameinstance[message.author].iterate(formattedlist[1], message.author))
            return
        await message.channel.send(embed = discord.Embed(title = "Invalid Entry", description="Use ~answer {a/A or b/B} to respond to a question.\nEnter ~game to see your question again"))

    if formattedlist[0] == '~highscore':
        if len(formattedlist) == 2:
            if not formattedlist[1] in user_db.userhighscore_name:
                print(user_db.userhighscore_name)
                await message.channel.send("No high score by this player")
                return
            await message.channel.send(f"{formattedlist[1]}'s high score: {user_db.userhighscore_name[formattedlist[1]]}")
            return
        else:
            await message.channel.send(embed = await game.gethighscores())

    
try :
    client.run(TOKEN)
except discord.errors.HTTPException:
    print("Token is broken, get a new one") 