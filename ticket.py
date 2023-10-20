#Structure of ticket
class Ticket:
    def __init__(self, name, reason):
        self.name = name            #Team name
        self.reason = reason        #Reason for help
        self.in_progress = False    #Are they currently being helped?

#Create ticket based on team name and reason
def create_ticket(team_name, reason):
    return Ticket(team_name, reason)