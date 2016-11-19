#The list of all objects to be simulated in the form (position, velocity, standard gravitational paramater, radius)[]
state = []

#Defines the starting conditions for the start of the simulation
#Returns a list of tupples where each tupple contains (parent_body, mass, radius, true_anomaly, apsis, periapsis, argument_of_periapsis)
#A starting angle of 0 indicates that the body is directly above (+y). Anti-clockwise, in radians.
def get_starting_conditions(file_name):

#Takes a list of tupples (parent_body, mass, radius, true_anomaly, apsis, periapsis, argument_of_periapsis) and returns
#a tupple continaing (position, velocity, standard gravitational paramater, radius).
#The orbital characteristics are defined relative to the center of mass of the whole system.
#If the mass is -1 then the body is a ficticious body only defined to define the starting conditions.
def convert_to_internal_representation(initial_state):

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
    
    state = convert_to_internal_representation(get_starting_conditions(filename))

    #FIX: This may need to be made global, atm it is unused.
    dt = input("Timestep:")
    
    initialise_display()
    show_simulation()

main()
