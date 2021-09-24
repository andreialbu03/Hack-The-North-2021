import discord


def get_help():
    helpEmbed = discord.Embed(title = "Help", description = "Covi was created to help people keep themselves informed on COVID-19.\nOur commands:", color = 0xb23831)
    helpEmbed.add_field(name = "~covid-global", value = "Displays global COVID-19-related statistics", inline = True)
    helpEmbed.add_field(name = "~covid [country]", value = "Displays country COVID-19-related statistics", inline = True)
    helpEmbed.add_field(name = "~covid-news [country (optional)]", value = "Displays one of the country's/globe's current top 3 COVID-19 news articles", inline = False)
    helpEmbed.add_field(name = "~tips", value = "Provides a random tip to keep you safe from COVID-19", inline = False)
    helpEmbed.add_field(name = "~game", value = "Starts a COVID-19-themed trivia game", inline = True)
    helpEmbed.add_field(name = "~answer [answer]", value = "To answer a game question", inline = True)
    helpEmbed.add_field(name = "~highscore", value = "Displays game leaderboard", inline = True)
    return helpEmbed