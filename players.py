class Player(object):

    def __init__(self, name=' ', team= ' ', goal = 0, redCards = 0, yellowCards = 0,\
                       subs=0, fantasyScore=0, apperances=0, position=' ', match = 0,score = 0,\
                       conceded = 0):
        self.name = name
        self.team = team
        self.goals = goal
        self.red = redCards
        self.yellow = yellowCards
        self.subs = subs
        self.points = fantasyScore
        self.starts = apperances
        self.pos = position
        self.match = match
        self.score = score
        self.conceded = conceded
        
    def __str__(self):
        string = ("%s plays as a %s for %s." % (self.name, self.pos, self.team))
        string += (" Making %s starts and %s as subs." % (self.starts,self.subs))
        string += (" Collecting %s red cards and %s yellow cards along the way." % (self.red,self.yellow))
        string += (" Scored %s goals and has %s fantasy points." % (self.goals,self.points))
        string += (" Fantasy Score %s and fantasy Conceded %s" % (self.score,self.conceded))
        return string
        
class Team(object):

    def __init__(self, name=' ',position= 0, goals = 0, conceded = 0, percentage = 0):
        self.name = name
        self.position = position
        self.goals = goals
        self.conceded = conceded
        self.percentage = percentage
        
    def __str__(self):
        string = ("%s are scoring %s and conceding %s goals and are %s in the league" % \
                      (self.name, self.goals, self.conceded, self.position))
    