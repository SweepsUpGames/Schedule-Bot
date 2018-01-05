#!/usr/bin/env python
import re
import socket
import time

from config import owl_schedule

_DELIMETER = '\r\n'

class NotConnectedError(Exception):
    def __init__(self):
        super.__init__("IRCBot is not connected to a channel!")

class TwitchBot(object):
    def __init__(self, host, port, nickname, password, channel):
        self._connection = None
        self._host = host
        self._port = port
        self._nickname = nickname
        self._password = password
        self._channel = _format_channel(channel)
        self._running = False
        self.line_num = 0

    def start(self):
        self._connect()
        self._running = True
        raw_data = ""
        while self._running:
            raw_data += self._connection.recv(1024).decode('UTF-8')
            lines, raw_data = raw_data.rsplit(_DELIMETER, 1)
            for line in lines.split(_DELIMETER):
                self.process_line(line)
            time.sleep(5)
        self._disconnect()

    def stop(self):
        self._running = False

    def process_line(self, line):
        print('{}: {}'.format(self.line_num, line))
        self.line_num += 1
        message = ping_parser(line) or owl_parser(line)
        if message:
            self._send(message)


    def send_message(self, message):
        self._check_connection()
        self._send('PRIVMSG {} :{}'.format(self._channel, message))

    def send_pong(self):
        self._check_connection()
        self._send('PONG :tmi.twitch.tv')

    def send_nickname(self):
        self._check_connection()
        self._send('NICK {}'.format(self._nickname))

    def send_password(self):
        self._check_connection()
        self._send('PASS {}'.format(self._password))

    def join_channel(self):
        self._check_connection()
        self._send('JOIN {}'.format(self._channel))

    def _send(self, message):
        print("Sending: {}".format(message))
        self._connection.send(bytes('{}\r\n'.format(message), "UTF-8"))

    def _connect(self):
        print("Opening connection to {}:{}...".format(self._host, self._port))
        self._connection = socket.socket()
        self._connection.connect((self._host, self._port))
        self.send_password()
        self.send_nickname()
        self.join_channel()

    def _disconnect(self):
        self._connection.close()
        self._connection = None

    def _check_connection(self):
        if self._connection is None:
            raise NotConnectedError()


def _format_channel(channel):
    if channel.startswith('#'):
        return channel
    return '#{}'.format(channel)


day_mod = {
    '1': 'st',
    '21': 'st',
    '31': 'st',
    '2': 'nd',
    '22': 'nd',
    '3': 'rd',
    '23': 'rd'
}
def _format_game(game):
    diff = game.countdown()
    matchup = "{} vs {}".format(game.home.fullname, game.away.fullname)
    if diff.days > 0:
        dow = game.game_datetime.strftime("%A")
        month = game.game_datetime.strftime("%B")
        day = game.game_datetime.strftime("%d")
        day_under = day_mod.get(day, 'th')
        hour = str(int(game.game_datetime.strftime("%I")))
        tod = game.game_datetime.strftime("%p")
        time_till = "on {}, {} {}{} at {} {}".format(dow, month, day, day_under, hour, tod)
    else:
        time = diff.seconds
        hours = time // 3600
        time -= hours * 3600
        minutes = time // 60
        time -= minutes * 60
        seconds = time
        if hours:
            msg = "in {} hour{}".format(hours, "s" if hours > 1 else "")
            if minutes:
                msg += " {} minute{}".format(minutes, "s" if minutes > 1 else "")
        elif minutes:
            msg = "in {} minute{}".format(minutes, "s" if minutes > 1 else "")
            msg += " {} second{}".format(seconds, "s" if seconds > 1 else "")

        time_till = "in {}".format(msg)
    return "{} {}".format(matchup, time_till)


def ping_parser(line):
    """When Twitch pings, the server ,ust pong back or be dropped."""
    if line == 'PING :tmi.twitch.tv':
        return 'PONG :tmi.twitch.tv'
    return None


def owl_parser(line):
    """Respond to !owl requests."""
    owl_re = r'^\:(\w*)\!\w*@\w*\.tmi\.twitch\.tv PRIVMSG #(\w*) \:(!owl.*)'
    results = re.match(owl_re, line)
    if not results:
        return None

    user = results.group(1)
    channel = results.group(2)
    command = results.group(3).strip()

    if command == '!owl':
        message = _format_game(owl_schedule.get_next())
    elif command.startswith('!owl '):
        owl_game = owl_schedule.get_next_for(command[5:])
        if owl_game:
            message = _format_game(owl_game)
        else:
            return None
    else:
        return None
    return 'PRIVMSG #{} :{}'.format(channel, message)
