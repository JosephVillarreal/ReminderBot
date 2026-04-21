# This example requires the 'message_content' intent.
# https://discordpy.readthedocs.io/en/stable/index.html

import discord
from discord.ext import tasks, commands
import datetime
import isodate
import sqlite3

class Reminder:
    def __init__(self):
        self.id = None
        self.role = None
        self.executeTime = None
        self.message = None
        self.channel = None

    def __str__(self):
        return (f'{self.id}, {self.role}, {self.executeTime}, {self.channel}, {self.message}')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

#Open our database to store stuff
databaseConnection = sqlite3.connect('reminder.db')
databaseCursor = databaseConnection.cursor()

# DEBUG ONLY
# databaseCursor.execute("DROP TABLE IF EXISTS reminderEntries")
# databaseConnection.commit()
# / DEBUG ONLY

databaseCursor.execute('''
CREATE TABLE IF NOT EXISTS reminderEntries (
    id INTEGER PRIMARY KEY,
    role TEXT,
    executeTime INTEGER,
    message TEXT,
    channel INTEGER
);
''')

helpMessage = """Discord Reminder Bot Help
Commands are always enclosed in by double quotation characters, separated by the pipe character, and consist of three parts:
Role - the role that the bot will ping when the timer expires. Do not include the `@` character. Roles are checked at reminder execution time. Invalid roles will not cause a ping.
    Example: `GUEST`, would ping the role with the same name, if that role exists.
Time Delta - Structure: P[n]Y[n]M[n]DT[n]H[n]M[n]S
    Example: 37 days, 1 hour, and 7 seconds = `P37DT1H7S`
Message - The message that you want the bot to display when the timer expires.
    Example $RemindMe "GUEST|PT10S|This example reminder will execute 10 seconds after ReminderBot sees it."

www.team-uber.com
"""

# Initialize
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    print(f'Reminder Bot is ready for use.')
    tick.start()

# tick
@tasks.loop(seconds=1.0)
async def tick():
    # On tick, have the database show us all entries that are YearMonthDayHourMinuteSecond less than current, then execute and clear all of those entries.
    currentTime = datetime.datetime.now()
    timeAsInteger = int(currentTime.timestamp())
    query = "SELECT * FROM reminderEntries WHERE executeTime < ?"
    databaseCursor.execute(query, (timeAsInteger,))

    entries = databaseCursor.fetchall()
    for entry in entries:
        reminder = Reminder()
        reminder.id = entry[0]
        reminder.role = entry[1]
        reminder.executeTime = datetime.datetime.fromtimestamp(entry[2])
        reminder.message = entry[3]
        reminder.channel = entry[4]

        await executeReminder(reminder)
        clearReminder(reminder)

# This runs whenever the bot sees `$RemindMe` in any channel it is part of.
@bot.command()
async def RemindMe(messageContext, input):
    try:
        currentTime = datetime.datetime.now()
        reminder = Reminder()
        parameters = input.split('|')

        # Get whatever role we're going to ping
        reminder.role = parameters[0]

        # Get when the reminder should be executed
        # isodate will parse a well-formed IS8601 delta string into a datetime delta object.
        duration = isodate.parse_duration(parameters[1])
        # Python's datetime 
        executeTime = currentTime + duration
        # Convert it into an integer number of seconds.
        reminder.executeTime = int(executeTime.timestamp())

        reminder.message = parameters[2]

        reminder.channel = messageContext.channel.id

        createReminder(reminder)
        await messageContext.send('Reminder stored.')

    except:
        # If they made a poorly formed command (including `$RemindMe "Help"`), reply with the help message.
        await messageContext.send(helpMessage)

# Helper functions
def createReminder(reminder):
    insert_query = """
    INSERT INTO reminderEntries (role, executeTime, message, channel)  VALUES (?, ?, ?, ?)
    """
    databaseCursor.execute(insert_query, (reminder.role, reminder.executeTime, reminder.message, reminder.channel))
    databaseConnection.commit()
    print(f"Created entry: {reminder}") 

def clearReminder(reminder):
    delete_query = """
    DELETE FROM reminderEntries WHERE id = ?
    """
    databaseCursor.execute(delete_query, (reminder.id,))
    databaseConnection.commit()
    print(f"Deleted entry: {reminder}") 

async def executeReminder(reminder):
    Ping = reminder.role
    channel = bot.get_channel(reminder.channel)
    for role in (channel.guild.roles):
        if role.name == reminder.role:
            Ping = role.id
            break
        
    output = f"<@&{Ping}>|{reminder.message}"

    await channel.send(output)
    print(f"Executed entry: {reminder}") 

# Main()
bot.run('')
