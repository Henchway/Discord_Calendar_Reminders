# https://realpython.com/how-to-make-a-discord-bot-python/

import datetime
import os

import discord
import pytz
import requests
from dotenv import load_dotenv
from icalendar import Calendar

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CALENDER_URL = os.getenv('CALENDER_URL')


def get_calender(url):
    return requests.get(url)


def get_todays_events(parsed_calendar):
    today = datetime.date.today()
    result = []
    for entry in parsed_calendar.walk():
        if entry.name == "VEVENT":
            start_date = entry.get("DTSTART").dt
            if type(start_date) == datetime.datetime:
                if start_date.date() == today:
                    summary = entry.get("summary")
                    description = entry.get("description")
                    result.append(dict(summary=summary, description=description, start_date=start_date))
    return result


raw_cal = get_calender(CALENDER_URL)
parsed_cal = Calendar.from_ical(raw_cal.content)
events = get_todays_events(parsed_cal)
client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    channels = await guild.fetch_channels()
    for channel in channels:
        for event in events:
            now = datetime.datetime.now(tz=pytz.timezone('Europe/Vienna'))
            remaining_minutes = (event.get("start_date") - now).seconds / 60
            if channel.name.replace("-", " ") in event.get(
                    "summary").lower() and 90 > remaining_minutes > 0:
                await channel.send(
                    f"{event.get('summary')}\n\n{event.get('start_date').astimezone(pytz.timezone('Europe/Vienna'))}\n\n{event.get('description')}")


client.run(TOKEN)
