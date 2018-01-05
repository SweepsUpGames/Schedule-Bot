"""Run the bot server."""
from bots import twitch_bot

SERVER = 'irc.chat.twitch.tv'
PORT = 6667
NICK = 'sirbottles'
PASS = 'oauth:vwd8pk6wgzo4relz17cjxensjr0czq'
CHANNEL = "#nothingatall544"

def run():
    """Function to start the server."""
    bot = twitch_bot.TwitchBot(SERVER, PORT, NICK, PASS, CHANNEL)
    bot.start()

if __name__ == "__main__":
    run()
