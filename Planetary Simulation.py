import types
import yaml
import math

from matplotlib import pyplot
from matplotlib import animation

G = 6.67408 * 10 ** -11

#Defines the starting conditions for the start of the simulation
#A starting angle of 0 indicates that the body is directly above (+y). Anti-clockwise, in radians.
#Returns a dictionary of dictionaires where each tupple contains (name, parent_body, mass, radius, true_anomaly, apsis, periapsis, longitude_of_periapsis, direction_of_rotation).
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
        initial_state = types.SimpleNamespace(**i)
        initial_state.direction_of_rotation = initial_state.direction_of_rotation == 'clockwise'
        object_list.append(initial_state)
    
        key_to_find = i['parent_body']
    
        if key_to_find in place_dict:
            initial_state.parent_body = place_dict[key_to_find]
    
    return object_list

#Takes a list of tupples (name, parent_body, mass, radius, true_anomaly, apsis, periapsis, longitude_of_periapsis, direction_of_rotation) and returns
#a tupple continaing (name, position, velocity, standard gravitational paramater, radius).
#The orbital characteristics are defined relative to the center of mass of the whole system.
#If the mass is -1 then the body is a ficticious body only defined to define the starting conditions.
def convert_to_internal_representation(initial_state):
    length = len(initial_state)
    
    global state
    state = [-1] * length
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
    
    position = types.SimpleNamespace()
    position.x = distance * math.cos(initial_value.true_anomaly)
    position.y = distance * math.sin(initial_value.true_anomaly)
    
    focal_length = semi_latus_rectum * ecc / (1 - ecc ** 2)
    zero_x = position.x - focal_length
    
    if abs(position.y * (ecc ** 2 - 1)) < 1e-16:
        if (zero_x < 0) != (initial_value.direction_of_rotation):
            velocity = types.SimpleNamespace(x = 0, y = -speed)
        else:
            velocity = types.SimpleNamespace(x = 0, y = speed)
    else:
        dydx = zero_x / (position.y * (ecc ** 2 - 1))
        denominator = 1 / math.sqrt(1 + dydx ** 2)
        velocity = types.SimpleNamespace(x = speed / denominator, y = velocity.x * dydx)
        
        if (position.y > 0) != (initial_value.direction_of_rotation):
            velocity.x = -velocity.x
            velocity.y = -velocity.y
    
    cos_theta = math.cos(initial_value.longitude_of_periapsis)
    sin_theta = math.sin(initial_value.longitude_of_periapsis)
    rotate(position, sin_theta, cos_theta)
    rotate(velocity, sin_theta, cos_theta)
    
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
    
def rotate(vector, sin, cos):
    x = vector.x
    y = vector.y
    vector.x = cos * x - sin * y
    vector.y = sin * x + cos * y
    
#Updates the display objects
def display(frame, patch_list):
    for i in range(0, len(patch_list)):
        patch_list[i].center = (state[i].position.x, state[i].position.y)
       
    simulate(dt)    

#Sets up the display objects for the animator and starts the simulations
def initialise_display():
    fig = pyplot.figure()
    
    patch_list = [pyplot.Circle((x.position.x, x.position.y), radius = x.radius) for x in state]
    for c in patch_list:
        pyplot.gca().add_patch(c)
        
    pyplot.axis('scaled')
    pyplot.title('Earth-Moon system')
    
    #This variable is needed due to some arcane garbage collection black magic
    unused = animation.FuncAnimation(fig, display, fargs = (patch_list, ), interval = 20)
    
    pyplot.show()

#Steps the things forward by timestep
def simulate(timestep):
    print('Not done')
    
def main():
    filename = input("Enter the filename for the initial starting conditions: ")
    
    convert_to_internal_representation(get_starting_conditions(filename))

    global dt 
    dt = input("Timestep:")
    
    initialise_display()
main()
