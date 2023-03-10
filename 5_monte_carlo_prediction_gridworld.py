# -*- coding: utf-8 -*-
"""5 - Monte Carlo Prediction GridWorld.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oZt_gvuQC6GeVHu5nJKh2Uawbcvnj9GM
"""

import GridWorld
import numpy as np

robot=GridWorld.grid_world()

def print_values(V, rows,columns):
    for i in range(rows):
        print("---------------------------")
        for j in range(columns):
            v = V.get((i,j), 0)
            if v >= 0:
                print(" %.2f|" % v, end="")
            else:
                print("%.2f|" % v, end="") # -ve sign takes up an extra space
        print("")

robot.step('U')

robot.s

### fixed policy ###
policy = {
    (2, 0): 'U',
    (1, 0): 'U',
    (0, 0): 'R',
    (0, 1): 'R',
    (0, 2): 'R',
    (1, 2): 'U',
    (2, 1): 'R',
    (2, 2): 'U',
    (2, 3): 'L',
  }

def play_episode(policy,max_steps=20):
    
    # keep track of all states and rewards encountered
    episodestates = [robot.initial_state()]
    episoderewards = [0]
    steps = 0
    done=False
    while not done:
        a = policy[robot.s]
        next_s,r,done=robot.step(a)
        episodestates.append(next_s)
        episoderewards.append(r)
        steps += 1
        if steps >= max_steps:
            break
    # we want to return:
    # gamestates  = [s(0), s(1), ..., S(T)]
    # gamerewards = [R(0), R(1), ..., R(T)]

    return episodestates, episoderewards

play_episode(policy,max_steps=20)

# initialize V(s) and returns
GAMMA=0.9
V = {}
returns = {} # dictionary of state -> list of returns we've received
for s in robot.States:
    if s in robot.actions.keys():
        returns[s] = []
    else:
        # terminal state or state we can't otherwise get to
        V[s] = 0
# repeat
for t in range(100):
    # generate an episode using pi
    episodestates, episoderewards = play_episode(policy,max_steps=20)
    G = 0
    T = len(episodestates)
    for t in range(T - 2, -1, -1):
        s = episodestates[t]
        r = episoderewards[t+1]
        G = r + GAMMA * G # update return

      # we'll use first-visit Monte Carlo
        if s not in episodestates[:t]:
            returns[s].append(G)
            V[s] = np.mean(returns[s])

print_values(V,3,4)

for t in range(5 - 2, -1, -1):
    print(t)

