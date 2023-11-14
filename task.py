class Task():

    def __init__(self, task):
        self.task = task
        self.team_in_charge = None
        self.channel = None
        self.completed = False

    #Assign task a team
    def assign_team(self, team_in_charge):
        self.team_in_charge = team_in_charge

    #Finished a task
    def completed(self):
        self.completed = True
        
    #Assign task a channel
    def assign_channel(self, channel):
        self.channel = channel

class TaskList():

    def __init__(self):
        self.list = []

    #Add task to list
    def add_task(self, task):
        self.list.append(task)
    
    #Find task by description
    def find(self, task):
        for task in self.list:
            if task.task == task:
                return task
        return None

#Create a task and add it to list of tasks
def create_task(task_list, description):
    task = Task(description)
    task_list.add_task(task)
    
    return task_list
