#Structure of ticket
class Ticket:
    def __init__(self, name, reason):
        self.name = name
        self.reason = reason

#Create ticket based on team name and reason
def create_ticket(team_name, reason):
    return Ticket(team_name, reason)