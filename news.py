from serpapi import GoogleSearch
import discord
import random
import ISO3166


#case 0: global information
async def get_covid_news_location(loc):

    gl = loc.upper() if len(loc) == 2 else ISO3166.ISO3166rev[str(loc).lower()]

    params = {
        "engine": "google",
        "q": "covid",
        "tbm": "nws",
        "gl": gl,
        "api_key": "7ab6ff1f1481fc90fd2508ff760c72a916af0e5e80c3f938dd84f28340ee2c1b",
    }

    search = GoogleSearch(params)

    news_results = search.get_dict().get("news_results")

    return await parse_covid_info_arr(news_results)


#case 1: local information
async def get_covid_news():
    params = {
        "engine": "google",
        "q": "covid",
        "tbm": "nws",
        "api_key": "7ab6ff1f1481fc90fd2508ff760c72a916af0e5e80c3f938dd84f28340ee2c1b",
    }

    search = GoogleSearch(params)

    news_results = search.get_dict().get("news_results")

    return await parse_covid_info_arr(news_results)


#layer in case we do multiple news post per command
async def parse_covid_info_arr(news_data):
    return await parse_covid_info(news_data[random.randint(0,2)])   #get one of top 3 results


async def parse_covid_info(index):
    output = discord.Embed(
        title = index["title"],
        url = index["link"],
        description = index["snippet"],
        color = 0xb23831,
    ).set_image(url = index["thumbnail"])
    return output

