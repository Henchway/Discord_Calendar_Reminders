#  Discord_Calendar_Reminders

It's required to include a .env file containing the following data:  

- DISCORD_TOKEN={Discord Bot Token}
- DISCORD_GUILD={Discord Server Name (Guild)}
- CALENDAR_URL={URL to the .ics file}
- MINUTES={Range of minutes within a message should be sent to the discord channel}

# Current Issues
On Windows systems the client.logout() / client.close() throw a runtime error. 
https://bugs.python.org/issue39232

On Linux this works without error.
