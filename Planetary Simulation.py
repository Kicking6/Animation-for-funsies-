#The list of all objects to be simulated in the form (position, velocity, standard gravitational paramater, radius)[]
state = []

#Defines the starting conditions for the start of the simulation
#Returns a list of tupples where each tupple contains (mass, radius, starting angle, apogee, perigee)
def get_starting_conditions(file_name):

#Takes a tupple (mass, radius, starting angle, apogee, perigee) and returns
#a tupple continaing (position, velocity, standard gravitational paramater, radius).
#The orbital characteristics are defined relative to the center of mass of the whole system.
def convert_to_internal_representation(thing_data):

#Sets up the display objects for the animator
def initialise_display():

#Updates the display objects
def display():

#Steps the things forward by timestep
def simulate(timestep):

#Displays the window and starts the animation, this will also start the phyiscal simulation
def show_simulation():

def main():
    filename = input("Enter the filename for the initial starting conditions:")
    state = [convert_to_internal_representation(thing) for thing in get_starting_conditions(filename)]

    #FIX: This may need to be made global, atm it is unused.
    dt = input("Timestep:")
    
    initialise_display()
    show_simulation()

main()
