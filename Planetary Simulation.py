import types
import yaml
import math

#The list of all objects to be simulated in the form (position, velocity, standard gravitational paramater, radius)[]
state = []
G = 6.67408 * 10 ** -11

#Defines the starting conditions for the start of the simulation
#Returns a dictionary of dictionaires where each tupple contains (name, parent_body, mass, radius, true_anomaly, apsis, periapsis, longitude_of_periapsis).
def get_starting_conditions(file_name):
    file_name = 'Starting Conditions.yaml'
    file = open(file_name, "r")
    contents = yaml.load(file)

    object_list = []
    place_dict = {}
    place = 0
    for i in contents:
        name = i['name'] 
        place_dict[name] = place
        place += 1

    for i in contents:
        initial_state = types.SimpleNamespace()
        initial_state.name = i['name']
        initial_state.parent_body = i['parent_body']
        initial_state.mass = i['mass']
        initial_state.radius = i['radius']
        initial_state.true_anomaly = i['true_anomaly']
        initial_state.apsis = i['apsis']
        initial_state.periapsis = i['periapsis']
        initial_state.longitude_of_periapsis = i['longitude_of_periapsis']
        object_list.append(initial_state)
    
        key_to_find = i['parent_body']
    
        if key_to_find in place_dict:
            initial_state.parent_body = place_dict[key_to_find]
    
    return object_list

#Takes a list of tupples (name, parent_body, mass, radius, true_anomaly, apsis, periapsis, longitude_of_periapsis) and returns
#a tupple continaing (name, position, velocity, standard gravitational paramater, radius).
#The orbital characteristics are defined relative to the center of mass of the whole system.
#If the mass is -1 then the body is a ficticious body only defined to define the starting conditions.
def convert_to_internal_representation(initial_state):
    length = len(initial_state)
    state.extend([-1] * length)
    for i in range(length):
        state[i] = convert_to_internal_representation_single(initial_state, i)
        
#converts a single element to the internal representation using index
def convert_to_internal_representation_single(initial_state, index):
    initial_value = initial_state[index]
    
    if len(state) > index and state[index] != -1:
        return state[index]
    
    parent_index = initial_value.parent_body
    if parent_index != -1:
        parent_body = convert_to_internal_representation_single(initial_state, parent_index)
    else:
        return types.SimpleNamespace(
            name = initial_value.name,
            position = types.SimpleNamespace(x = 0, y = 0, z = 0), 
            velocity = types.SimpleNamespace(x = 0, y = 0, z = 0), 
            GM = G * initial_value.mass, 
            radius = initial_value.radius
        )
        
    ecc = (initial_value.apsis - initial_value.periapsis) / (initial_value.apsis + initial_value.periapsis)
    semi_latus_rectum = 2 / (1 / initial_value.apsis + 1 / initial_value.periapsis)
    distance = semi_latus_rectum / (1 + ecc * math.cos(initial_value.true_anomaly))
    speed = math.sqrt(parent_body.GM * (2 / distance))
    
    #TODO take into account longitude_of_periapsis
    
    position = types.SimpleNamespace()
    position.x = distance * math.sin(initial_value.true_anomaly)
    position.y = distance * math.cos(initial_value.true_anomaly)
    
    dydx = position.x / (position.y * (ecc ** 2 - 1))
    denominator = 1 / math.sqrt(1 + dydx ** 2)
    
    velocity = types.SimpleNamespace()
    velocity.x = speed / denominator
    velocity.y = velocity.x * dydx
    
    thing = types.SimpleNamespace()
    thing.position = position
    thing.velocity = velocity
    thing.GM = G * initial_value.mass
    thing.radius = initial_value.radius
    thing.name = initial_value.name
    
    thing.position.x += parent_body.position.x
    thing.position.y += parent_body.position.y
    thing.velocity.x += parent_body.velocity.x
    thing.velocity.y += parent_body.velocity.y
    
    return thing
    
#Sets up the display objects for the animator
def initialise_display():
    print('Not done')
    
#Updates the display objects
def display():
    print('Not done')
    
#Steps the things forward by timestep
def simulate(timestep):
    print('Not done')
    
#Displays the window and starts the animation, this will also start the phyiscal simulation
def show_simulation():
    print('Not done')
    
def main():
    filename = input("Enter the filename for the initial starting conditions: ")
    
    convert_to_internal_representation(get_starting_conditions(filename))

    #FIX: This may need to be made global, atm it is unused.
    dt = input("Timestep:")
    
    initialise_display()
    show_simulation()

main()
