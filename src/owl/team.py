"""Represents an Overwatch League Team."""
class Team(object):
    def __init__(self, nickname, fullname):
        self.nickname = nickname.lower()
        self.fullname = fullname

    def __eq__(self, other):
        if isinstance(other, str):
            return self.nickname == other.lower()

    def __repr__(self):
        return "OWL: {}".format(self.fullname)
