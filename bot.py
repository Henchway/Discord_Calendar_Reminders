# https://realpython.com/how-to-make-a-discord-bot-python/
import datetime
import os

import aiohttp
import discord
import pytz
from dotenv import load_dotenv
from icalendar import Calendar

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CALENDAR_URL = os.getenv('CALENDAR_URL')

client = discord.Client()


async def get_calendar():
    async with aiohttp.ClientSession() as session:
        async with session.get(CALENDAR_URL) as response:
            return await response.text()


async def get_todays_events():
    cal_response = await get_calendar()
    parsed_calendar = Calendar.from_ical(cal_response)
    today = datetime.date.today()
    all_events = (entry for entry in parsed_calendar.walk() if entry.name == "VEVENT")
    events_with_datetime = (entry for entry in all_events if isinstance(entry.get("DTSTART").dt, datetime.datetime))
    return (entry for entry in events_with_datetime if entry.get("DTSTART").dt.date() == today)


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    channels = await guild.fetch_channels()
    events = await get_todays_events()
    now = datetime.datetime.now(tz=pytz.timezone('Europe/Vienna'))

    for event in events:
        for channel in channels:
            remaining_minutes = (event.get("DTSTART").dt - now).seconds / 60
            if channel.name.replace("-", " ") in event.get(
                    "summary").lower() and 90 > remaining_minutes > 0:
                await channel.send(
                    f"{event.get('summary')}\n\n{event.get('DTSTART').dt.astimezone(pytz.timezone('Europe/Vienna'))}\n\n{event.get('description')}")
    await client.logout()


# loop = asyncio.get_event_loop()
# loop.run_until_complete(client.start(TOKEN))

client.run(TOKEN)
