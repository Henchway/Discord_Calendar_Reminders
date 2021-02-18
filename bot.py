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
    all_events = (entry for entry in parsed_calendar.walk() if entry.name == "VEVENT")
    events_with_datetime = (entry for entry in all_events if isinstance(entry.get("DTSTART").dt, datetime.datetime))
    return (entry for entry in events_with_datetime if entry.get("DTSTART").dt.date() == today)


raw_cal = get_calender(CALENDER_URL)
parsed_cal = Calendar.from_ical(raw_cal.content)
events = get_todays_events(parsed_cal)
client = discord.Client()


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    channels = await guild.fetch_channels()
    now = datetime.datetime.now(tz=pytz.timezone('Europe/Vienna'))

    for event in events:
        for channel in channels:
            remaining_minutes = (event.get("DTSTART").dt - now).seconds / 60
            if channel.name.replace("-", " ") in event.get(
                    "summary").lower() and 90 > remaining_minutes > 0:
                await channel.send(
                    f"{event.get('summary')}\n\n{event.get('DTSTART').dt.astimezone(pytz.timezone('Europe/Vienna'))}\n\n{event.get('description')}")
    print("Finished")


client.run(TOKEN)
