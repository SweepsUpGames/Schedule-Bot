from src.owl import team

def test_equals():
    unit_under_test = team.Team("Outlaws", "Houston Outlaws")
    assert unit_under_test == 'outlaws'
    assert unit_under_test == 'Outlaws'

def test_repr():
    unit_under_test = team.Team("Outlaws", "Houston Outlaws")
    assert str(unit_under_test) == 'OWL: Houston Outlaws'

def test_find():
    unit_under_test = [team.Team("Outlaws", "Houston Outlaws")]
    assert 'outlaws' in unit_under_test
