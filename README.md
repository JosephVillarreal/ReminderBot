# ReminderBot
A Discord reminder bot

To deploy the bot, you will need to get a Discord API Key.

Go to this website:
https://discord.com/developers/applications

Sign in.
Select "New Application".
Name it whatever you want (probably "RemindMe" or something useful).
On the left navigation bar select "Bot".
You'll need to enter your Discord password again to get to this page.
Then where it says "Token", select "Reset Token".
Copy that token, we will need it later.
Scroll down to "Message Content Intent", and turn it on by selecting the rocker toggle.
That should be it for configuration on Discord's side.

Now get the ReminderBot code, on the last line, inside the single quotation marks, put token you copied earlier.
It should look something like this:
```
bot.run('MTQ5NTk5NjE0ODUzMDQxMzYyOA.Gw-aFL.TbxasUvaZRluhM1ZKAvUICLqzdJ-MrIvYepeAo')
```

Save that. That is now your complete script.

Now go to your Ubuntu Server or Arch computer that will run the ReminderBot.
Create a Service File in /etc/systemd/system/
Name it "ReminderBot.service" (or whatever you want).

The content of the service file should be:
```
    [Unit]
    Description=Discord Reminder Bot
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 /home/USER/ReminderBot.py
    WorkingDirectory=/home/USER/
    StandardOutput=inherit
    StandardError=inherit
    Restart=always
    User=yourusername

    [Install]
    WantedBy=multi-user.target
```

You will need to replace both instances of "USER" above with your actual user account name.
You'll need to install some of the python libraries that ReminderBot uses.
Run:
```
sudo apt update
sudo apt install python3-pip
```

Then you are ready to install the libraries themselves. Run:
```
python3 -m pip install "discord"
python3 -m pip install "isodate"
```

Now create the script itself in your user's home directory.
You can test the script to ensure that it works properly by just running it. If it runs, you're ready to deploy it as a service.
To deploy it, run:
```
sudo systemctl daemon-reload
sudo systemctl enable ReminderBot
sudo systemctl start ReminderBot
```

ReminderBot should be working for you.

Here is ReminderBot's help example (idk how to turn word wrap on, scroll to the right or something):
```
8:41 PM]zelklen: $RemindMe -help
[8:41 PM] 
APP
 ReminderBot: Discord Reminder Bot Help
Commands are always enclosed in by double quotation characters, separated by the pipe character, and consist of three parts:
Role - the role that the bot will ping when the timer expires. Do not include the @ character. Roles are checked at reminder execution time. Invalid roles will not cause a ping.
    Example: GUEST, would ping the role with the same name, if that role exists.
Time Delta - Structure: P[n]Y[n]M[n]DT[n]H[n]M[n]S
    Example: 37 days, 1 hour, and 7 seconds = P37DT1H7S
Message - The message that you want the bot to display when the timer expires.
    Example $RemindMe "GUEST|PT10S|This example reminder will execute 10 seconds after ReminderBot sees it."

www.team-uber.com
```
