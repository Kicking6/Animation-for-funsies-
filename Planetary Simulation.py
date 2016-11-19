#Defines the starting conditions for the start of the simulation
#Returns a list of tupples where each tupple contains (eccentricity, starting angle, apogee, perigee)
def get_starting_conditions(file_name):
    perigee = 12
    apogee = 14
    return [(0.9, 0, apogee, perigee)]

#Takes a tupple (eccentricity, starting angle, apogee, perigee) and returns
#a tupple continaing (position, mass, radius, velocity)
def convert_to_internal_representation(thing_data):

#Sets up the display objects for the animator
def initialise_display(things):

#Updates the display objects
def display(things):
    "Does stuff"
    #TODO

#Steps the things forward by timestep
def simulate(timestep, things):
    #TODO

#Displays the window and starts the animation, this will also start the phyiscal simulation
def show_simulation(things):

def main():
    filename = input("Enter the filename for the initial starting conditions:")
    conditions = [convert_to_internal_representation(thing) for thing in get_starting_conditions(filename)]
    dt = input("Timestep:")
    initialise_display(conditions)
    show_simulation(conditions)

main()
