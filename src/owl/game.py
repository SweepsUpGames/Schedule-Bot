import datetime
import pytz


class OWLGame(object):
    def __init__(self, game_datetime, home, away):
        self.game_datetime = game_datetime
        self.home = home
        self.away = away

    def is_playing(self, team):
        return team in [self.home, self.away]

    def countdown(self):
        return self.game_datetime - datetime.datetime.now(tz=pytz.timezone('US/Pacific-New'))
