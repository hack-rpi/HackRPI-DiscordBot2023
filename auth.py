
#Auth check for certain commands
def authorized(author):
    authorized_individuals = ["Director", "President", "Vice-President", "Jr. Director", "Mentors"]

    for role in authorized_individuals:
        if role.lower() in [y.name.lower() for y in author.roles]:
            return True
    return False