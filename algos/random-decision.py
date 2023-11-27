"""
random-decision.py

This file implements a policy that randomly picks one of the five moves available every timestep:
down, left, right, rotate left, and rotate right.
"""
import random
import sys
from tqdm import tqdm

NUM_ITERATIONS = 100000

def main():

    if len(sys.argv) != 3:
        raise Exception("usage: python3 main.py <raw-dataset>.csv <output>.policy")

    # TODO: generate stuff based on either np.random or the random class by picking a number

    print("finished!")

if __name__ == '__main__':
    main()
