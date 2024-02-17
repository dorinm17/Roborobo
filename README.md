# PaintWars Roborobo

# Manea Dorin-Mihai & Draghici Mara-Andreea

### February, 2024

This project is written in Python and implements Braitenberg vehicles designed
using behaviour trees, using the [Roborobo simulator](https://github.com/nekonaute/SU-LU3IN025-robots/).
Two teams of eight robots each, that do not communicate with each other,
compete to paint as much of the map as possible with their team's color (Red or
Blue). One cell of the map can be repainted by the other team that happens to
pass by there.

*To run*: unzip the archive `logs.zip` and run the `go_tournament_eval`
executable. It will launch a tournament of different arenas and different start
positions. Alternatively, run `paintwars.py` for a single match.\
*To configurate*: `paintwars_config.py`\
Our algorithm is in `paintwars_sarmale.py`. By default, it competes with the
basic implemenation `paintwars_team_champion`.\\

Each robot has 8 sensors: front, front-left, front-right, left, right, back,
back-left, back-right. They distinguish between the different type of obstacles
(walls or other robots) and return values ranging from 1 (infinite distance) to
0 (next to). A linear combination of these values and excitatory (+1) or
inhibitory (-1) parameters controls the speed of transposition (1 - full speed
forward; -1 - full speed backward) and the speed of rotation (1 - 90 deg the
right; -1 - 90 deg to the left).\\

The algorithm prioritizes the avoidance of wall and same team robots,
respectively. Next, some robots are designed to follow robots from the opposite
team, if detected in proximity, to repaint their occupied cells. All robots
explore the map using a genetic algorithm based on mutation (mu=1, lambda=1) to
find the best parameters for controlling speed. Escaping measures in case of
becoming stuck have been taken into consideration.

Have fun at it!
