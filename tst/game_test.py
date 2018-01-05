import datetime
import pytz

from src.owl import game
from src.owl import team


TEAM_1 = team.Team('Shock', 'San Francisco Shock')
TEAM_2 = team.Team('Valiant', 'Los Angeles Valiant')
TEAM_3 = team.Team('Outlaws', 'Houston Outlaws')
TIME = datetime.datetime(2017, 1, 10, 16, tzinfo=pytz.timezone('US/Pacific-New'))

def test_playing():
    unit_under_test = game.OWLGame(TIME, TEAM_1, TEAM_2)
    assert unit_under_test.is_playing('shock')
    assert unit_under_test.is_playing(TEAM_1)
    assert unit_under_test.is_playing('valiant')
    assert unit_under_test.is_playing(TEAM_2)
    assert not unit_under_test.is_playing('outlaws')
    assert not unit_under_test.is_playing(TEAM_3)
