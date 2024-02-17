# Projet "robotique" IA&Jeux 2024
#
# Binome:
#  Prénom Nom: Dorin-Mihai Manea, 21302798
#  Prénom Nom: Mara-Andreea Draghici, 21302782

import random
import math
import numpy as np

# Romanian national dish - cabbage rolls
def get_team_name():
    return "Sarmale"

# added functionality to check the distance from a same or opposite team robot
# distance between 0 (next to) and 1 (infinity)
def get_extended_sensors(sensors):
    for key in sensors:
        sensors[key]["distance_to_robot"] = 1.0
        sensors[key]["distance_to_wall"] = 1.0
        sensors[key]["distance_to_my_robot"] = 1.0
        sensors[key]["distance_to_other_robot"] = 1.0

        if sensors[key]["isRobot"] == True:
            sensors[key]["distance_to_robot"] = sensors[key]["distance"]
            
            if sensors[key]["isSameTeam"] == True:
                sensors[key]["distance_to_my_robot"] = sensors[key]["distance"]
            else:
                sensors[key]["distance_to_other_robot"] = sensors[key]["distance"]
        else:
            sensors[key]["distance_to_wall"] = sensors[key]["distance"]

    return sensors

# if wall detected in front, slow down to avoid collision
# if wall detected in the front left, rotate to the right
# if wall detected in the front right, rotate to the left
def fear_wall(sensors):
    translation = 1 * sensors["sensor_front"]["distance_to_wall"]
    rotation = (-1) * sensors["sensor_front_left"]["distance_to_wall"] + 1 * sensors["sensor_front_right"]["distance_to_wall"]

    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))

    return translation, rotation

# if same team robot detected in front, slow down to avoid collision
# if same team robot in the front left, rotate to the right
# if same team robot in the front right, rotate to the left
def fear_my_robot(sensors):
    translation = 1 * sensors["sensor_front"]["distance_to_my_robot"]
    rotation = (-1) * sensors["sensor_front_left"]["distance_to_my_robot"] + 1 * sensors["sensor_front_right"]["distance_to_my_robot"]

    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))

    return translation, rotation

# conquering the cells occupied by the opposite team, slowing down to avoid collision
# if opposite team robot to the left, rotate to the left
# if opposite team robot to the right, rotate to the right
def love_other_robot(sensors):
    translation = 1 * sensors["sensor_front"]["distance_to_my_robot"]
    rotation = 1 * sensors["sensor_left"]["distance_to_other_robot"] + (-1) * sensors["sensor_right"]["distance_to_other_robot"]
    
    translation = max(-1,min(translation,1))
    rotation = max(-1, min(rotation, 1))

    return translation, rotation

# genetic algorithm that implements mutation (mu = 1, lambda = 1)
#    score = translation_speed * (1 - abs(rotation_speed))
# first generation is selected randomly;
# for the other generations, we randomly change one parameter of the current candidate solution
# and keep the solution with the bigger score
def explore(sensors):
    candidate_sol = np.array([random.randint(-1, 1) for _ in range(16)])
    sensors_distances = np.array([sensors[key]["distance"] for key in sensors])
    
    for _ in range(50):
        translation = math.tanh(sum(candidate_sol[:8] * sensors_distances))
        rotation = math.tanh(sum(candidate_sol[8:] * sensors_distances))
        score_parent = translation * (1 - math.fabs(rotation))

        change = random.randint(0, 15)
        old = candidate_sol[change]
        new = candidate_sol[change]

        while new == old:
            new=random.randint(-1,1)

        candidate_sol[change] = new
        translation = math.tanh(sum(candidate_sol[:8] * sensors_distances))
        rotation = math.tanh(sum(candidate_sol[8:] * sensors_distances))
        score_child = translation * (1 - math.fabs(rotation))
        
        if score_child <= score_parent:
            candidate_sol[change] = old

    translation = math.tanh(sum(candidate_sol[:8] * sensors_distances))
    rotation = math.tanh(sum(candidate_sol[8:] * sensors_distances))

    return translation, rotation
    
    
# maximizing the chance of getting out by randomizing the direction of the rotation
def check_if_stuck(translation, rotation):
    if math.fabs(translation) < 0.2 and math.fabs(rotation) < 0.2:
        translation = -1
        rotation = random.choice([-1, 1])

    return translation, rotation

# behaviour tree architecture
def step(robotId, sensors):
    translation = 1 # vitesse de translation (entre -1 et +1)
    rotation = 0 # vitesse de rotation (entre -1 et +1)
    sensors = get_extended_sensors(sensors)

    translation, rotation = fear_wall(sensors)

    if not (translation, rotation) == (1, 0):
        translation, rotation = check_if_stuck(translation, rotation)
        return translation, rotation

    translation, rotation = fear_my_robot(sensors)

    if not (translation, rotation) == (1, 0):
        translation, rotation = check_if_stuck(translation, rotation)
        return translation, rotation

    if robotId == 2 or robotId == 3 or robotId == 5 or robotId == 6:
    	translation, rotation = love_other_robot(sensors)

    if not (translation, rotation) == (1, 0):
        translation, rotation = check_if_stuck(translation, rotation)
        return translation, rotation

    translation, rotation = explore(sensors)
    return translation, rotation

