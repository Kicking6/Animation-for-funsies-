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
    file = open(file_name, "r")
    contents = yaml.load(file)

    global scale
    scale = contents['starting_scale']
    contents = contents['objects']

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
    speed = math.sqrt(parent_body.GM * (2 / distance - 1 / semi_latus_rectum))
    
    print(initial_value.name + ": " + str(speed))
    
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
        velocity = types.SimpleNamespace(x = speed / denominator, y = speed / denominator * dydx)
        
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
       
    for i in range(100):
        simulate(dt)  
    
    pyplot.title("Earth-Moon system. E = %.4e" % energy())

#Potential energy and kinetic
def energy():
    total_energy = 0
    for i in range(len(state)):
        kinetic_energy = 0.5 * state[i].GM / G * lengthSq(state[i].velocity)
        total_energy += kinetic_energy
        for j in range(i + 1, len(state)):
            potential_energy = - (state[i].GM * (state[j].GM / G)) / (lengthSq(vector_subtraction(state[i].position, state[j].position))) ** 0.5
            total_energy += potential_energy
      
    return total_energy
    
#Sets up the display objects for the animator and starts the simulations
def initialise_display():
    fig = pyplot.figure()
    
    patch_list = [pyplot.Circle((x.position.x, x.position.y), radius = x.radius) for x in state]
    for c in patch_list:
        pyplot.gca().add_patch(c)
        
    pyplot.axis([scale, -scale, scale, -scale])
    
    #This variable is needed due to some arcane garbage collection black magic
    unused = animation.FuncAnimation(fig, display, fargs = (patch_list, ), interval = 20)
    
    pyplot.show()

#Steps the things forward by timestep
def simulate(timestep):
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            thing1 = state[i]
            thing2 = state[j]
            
            #F = GMm / r^2
            
            delta = types.SimpleNamespace(x = thing1.position.x - thing2.position.x, y = thing1.position.y - thing2.position.y)
            r2 = lengthSq(delta)
            
            delta.x = delta.x / math.sqrt(r2)
            delta.y = delta.y / math.sqrt(r2)
            
            deltaV1 = timestep * thing2.GM / r2
            deltaV2 = timestep * thing1.GM / r2
            
            thing1.velocity.x -= delta.x * deltaV1
            thing1.velocity.y -= delta.y * deltaV1
            #thing1.velocity.z += deltaV1.z
    
            thing2.velocity.x += delta.x * deltaV2
            thing2.velocity.y += delta.y * deltaV2
            #thing2.velocity.z += deltaV1.z
            
    for i in range(len(state)):
        state[i].position.x += state[i].velocity.x * timestep
        state[i].position.y += state[i].velocity.y * timestep
            
def lengthSq(vec):
    return vec.x ** 2 + vec.y ** 2
    
#vec1 & vec2 is the input, returns vec1 - vec2.
# 2d!!!!!!!!!!!!!!
def vector_subtraction(vec1, vec2):
    vec = types.SimpleNamespace(x = 0, y = 0)
    vec.x = vec1.x - vec2.x
    vec.y = vec1.y - vec2.y
    #vec.z = vec1.z - vec2.z
    return vec

def main():
    filename = input("Enter the filename for the initial starting conditions: ")
    
    convert_to_internal_representation(get_starting_conditions(filename))

    global dt 
    dt = float(input("Timestep: "))
    
    initialise_display()
main()
