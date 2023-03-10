# -*- coding: utf-8 -*-
"""4 - Policy Iteration GridWorld.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Bw90SeIW_KWV9BCIehbWlg5sldevQm2V
"""

import numpy as np

#Initialization
ACTION_SPACE = ('U', 'D', 'L', 'R')
States=[(0, 0),
 (0, 1),
 (0, 2),
 (0, 3),
 (1, 0),
 (1, 2),
 (1, 3),
 (2, 0),
 (2, 1),
 (2, 2),
 (2, 3)]
REWARDS = {(0, 3): 1, (1, 3): -1}
actions = {
    (0, 0): ('D', 'R'),
    (0, 1): ('L', 'R'),
    (0, 2): ('L', 'D', 'R'),
    (1, 0): ('U', 'D'),
    (1, 2): ('U', 'D', 'R'),
    (2, 0): ('U', 'R'),
    (2, 1): ('L', 'R'),
    (2, 2): ('L', 'R', 'U'),
    (2, 3): ('L', 'U'),
    }

def is_terminal(s):
    return s in [(0, 3),(1, 3)]

is_terminal((2,3))

def get_next_state(s, a):
    # this answers: where would I end up if I perform action 'a' in state 's'?
    i, j = s[0], s[1]
    # if this action moves you somewhere else, then it will be in this dictionary
    if a in actions[(i, j)]:
        if a == 'U':
            i -= 1
        elif a == 'D':
            i += 1
        elif a == 'R':
            j += 1
        elif a == 'L':
            j -= 1
    return i, j

### define transition probabilities
  # the key is (s, a, s'), the value is the probability
  # that is, transition_probs[(s, a, s')] = p(s' | s, a)
  # any key NOT present will considered to be impossible (i.e. probability 0)
transition_probs = {}
  # to reduce the dimensionality of the dictionary, we'll use deterministic
  # rewards, r(s, a, s')
  # note: you could make it simpler by using r(s') since the reward doesn't
  # actually depend on (s, a)
rewards = {}


for s in States:
    if not is_terminal(s):
        for a in ACTION_SPACE:
            s2 = get_next_state(s, a)
            transition_probs[(s, a, s2)] = 1
            if s2 in REWARDS:
                rewards[(s, a, s2)] = REWARDS[s2]
            else:
                rewards[(s, a, s2)] = 0

transition_probs

rewards

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

policy.get((2,0))

transition_probs.get(((0, 0), 'U', (0, 0)))

def policy_evaluation(policy):
    # initialize V(s) = 0
    V = {}
    for s in States:
        V[s] = 0
    SMALL_ENOUGH = 1e-3 # threshold for convergence
    gamma = 0.9 # discount factor
    # repeat until convergence
    it = 0
    while True:
        biggest_change = 0
        for s in States:
            
            if is_terminal(s):
                V[s]=0
            else:
                old_v=V[s]
                new_v = 0 # we will accumulate the answer
                a=policy.get(s)
                for s2 in States:
                    r = rewards.get((s, a, s2),0)
                    new_v += transition_probs.get((s, a, s2),0) * (r + gamma * V[s2])
                # after done getting the new value, update the value table
                V[s] = new_v
                biggest_change = max(biggest_change, np.abs(old_v - V[s]))
        print("iter:", it, "biggest_change:", biggest_change)
        it += 1
        if biggest_change < SMALL_ENOUGH:
            break
    print("\n\n")
    return(V)

Values=policy_evaluation(policy)

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

print_values(Values, 3,4)

Values

for s in actions.keys():
    policy[s] = np.random.choice(actions.get(s))
policy

while True:
    gamma = 0.9
    # policy evaluation step - we already know how to do this!
    print(policy)
    V = policy_evaluation(policy)
    # policy improvement step
    is_policy_converged = True
    for s in States:
        if not is_terminal(s):
            old_a = policy[s]
            new_a = None
            best_value = float('-inf')
            # loop through all possible actions to find the best current action
            for a in actions.get(s):
                v = 0
                for s2 in States:
                # reward is a function of (s, a, s'), 0 if not specified
                    r = rewards.get((s, a, s2), 0)
                    v += transition_probs.get((s, a, s2), 0) * (r + gamma * V[s2])
                if v > best_value:
                    best_value = v
                    new_a = a
                  # new_a now represents the best action in this state
                    policy[s] = new_a
            if new_a != old_a:
                is_policy_converged = False
    if is_policy_converged:
        break

def print_policy(policy,rows,columns):
    for i in range(rows):
        print("---------------------------")
        for j in range(columns):
              a = policy.get((i,j), ' ')
              print("  %s  |" % a, end="")
        print("")

print_policy(policy,rows=3,columns=4)

