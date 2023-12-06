"""
q-learning.py

This file implements the main algorithm for generating the policy for a given dataset.
It uses q-learning and e-greedy to generate an output

usage:
python3 q-learning.py <dataset>.csv <output>.policy

To see how we create the dataset, please see generate-sars-data.py.
"""

import sys

import pandas as pd
import numpy as np
from tqdm import tqdm

# from ..app_utils.app_utils import Bot

NUM_TOTAL_REPEATS = 5

NUM_ITERATIONS = 10000000
MAX_ROLLOUT = 500

# parameters for Epsilon Greedy Exploration
EPSILON = 0.5
MIN_EPSILON = 0.1
E_DECAY = 0.95

# Parameters for Q-Learning
ALPHA = 0.001 # Learning rate
GAMMA =  0.95 # Discount Factor, can also be 1 depending on dataset


# Given s and a, returns the reward and an sp that is generated based
# on the probabilities for a given state and action.
# Assumes that there is at least 1 recorded action we can take.
def take_action(s, a, sa_r, sa_sp, probs):
    """
    pseudocode:
    1. given s & a, get list of sp-s from sa_sp
    2. do sequential inclusive scan, first value that's greater than randomly generated action is sp
    """
    r = sa_r[(s, a)] # 1-indexed
    sps = sa_sp[(s, a)]
    total = 0.0
    rand = np.random.rand()
    for sp in sps:
        total += probs[(s, a, sp)]
        if rand < total:
            return r, sp
    raise Exception('what the hell?!?')


# Policy (Pi) function for Epsilon Greedy Exploration.
def policy(q, s, s_a, e):
    a_l = np.array(list(s_a[s]))
    if (np.random.rand() < e):
        return np.random.choice(a_l)
    actions = q[s, :]
    avail_actions = actions[a_l]
    top = np.argmax(avail_actions) # a_l filters out by indices in a_l
    return a_l[top]

# helper fn.; given the name for a dataset, computes the reward for a given state,
# the set of actions for a given state, the set of potential next states
# for a given state and action, and the probability of advancng to a given
# future state given the current state, action and future state.
def precompute(dataset_filename):
    df = pd.read_csv(dataset_filename)
    # create initial dictionary: for each state and action, store all stuff from files
    sa_r = {} # state to reward
    d = {}
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        s, a = row['s'], row['a'] + 1 # make a 1-indexed inside this function so we can tell when a specific state
        r, sp = row['r'], row['sp']   # has not been visited

        if s not in d:
            d[s] = [[], [], []] # list of actions, then corresponding rewards, then corresponding next states
        sa_r[(s, a)] = r
        d[s][0].append(a)
        # d[row['s']][1].append(row['r'])
        d[s][2].append(sp)
    # create 2nd dictionary: for each key=(state, action, unique sp), store the probability of going to that sp
    probs = {}
    totals = {}
    for s in d:
        for i in range(len(d[s][0])):
            a, sp = d[s][0][i], d[s][2][i]
            if (s, a, sp) not in probs:
                probs[(s, a, sp)] = 0
            if (s, a) not in totals:
                totals[(s, a)] = 0
            probs[(s, a, sp)] += 1
            totals[(s, a)] += 1
    for s, a, sp in probs: # takes average by dividing over all possibilities for the given action
        probs[(s, a, sp)] /= totals[(s, a)]
    # create other final dictionaries: state to actions, state and action to sps
    actions = set()
    s_a = {}
    for s, a in totals:
        if s not in s_a:
            s_a[s] = set()
        s_a[s].add(a)
        actions.add(a)
    sa_sp = {}
    for s, a, sp in probs:
        if (s, a) not in sa_sp:
            sa_sp[(s, a)] = set()
        sa_sp[(s, a)].add(sp)
    return sa_r, s_a, sa_sp, probs, actions


def main():
    # Starting values! ----------------------
    e = EPSILON
    # ---------------------------------------
    if len(sys.argv) != 3:
        raise Exception("usage: python3 main.py <raw-dataset>.csv <output>.policy")

    dataset_filename = sys.argv[1]
    output_filename = sys.argv[2]
    print("Starting precomputing...")
    sa_r, s_a, sa_sp, probs, actions = precompute(dataset_filename) # NOTE: 1-indexed!
    num_s = max(s_a)
    num_a = len(actions)
    q = np.zeros((num_s + 1, num_a + 1)) # make everything 1-indexed for simplicity

    for i in range(NUM_TOTAL_REPEATS):
        print("Starting iterations ("+str(i+1)+'/'+str(NUM_TOTAL_REPEATS)+")...")
        for _ in tqdm(range(NUM_ITERATIONS)):
            # pick random first starting state
            s = np.random.randint(1, q.shape[0]) # TODO: pick out of the 1 of 2 starting states
            for _ in range(MAX_ROLLOUT):
                # No actions for a state means we have reached a dead-end
                if s not in s_a:
                    break

                a = policy(q, s, s_a, e)
                if (s, a) not in sa_sp:
                    print("\nwarning!")
                # Take action, observe next state and reward
                r, sp = take_action(s, a, sa_r, sa_sp, probs) 
                # Q-learning update rule
                # print(ALPHA * (r + GAMMA * np.max(q[sp,:]) - q[s,a]))
                q[s,a] += ALPHA * (r + GAMMA * np.max(q[sp,:]) - q[s,a])
                # Move to the next state
                s = sp
            # Decay epsilon over time
            e = max(MIN_EPSILON, e * E_DECAY)

        # Generate policy and save towards value
        print('Generating policy...')
        final_p = np.argmax(q, axis=1)[1:] # throws out placeholder for 1st value
        bueno = 0
        v = 0
        for i in tqdm(range(len(final_p))):
            if final_p[i] == 0:
                final_p[i] = np.random.randint(1, q.shape[1])
            else:
                v += max(0, q[i, final_p[i]])
                bueno += 1
        print('We have', bueno, 'nonrandom actions, expected 437399')
        print('Found mean best q of', v / bueno)
        print('Writing file...')
        np.savetxt(output_filename, final_p, delimiter=',', fmt='%s')
        print('Beginning evaluation...')
        # testbot = Bot(output_filename)

    print("Finished!")

if __name__ == '__main__':
    main()
