"""
random-decision.py

This file implements a policy that randomly picks one of the five moves available every timestep:
down, left, right, rotate left, and rotate right.

usage: python3 random-decision.py <output>.policy
"""

# some constants specific for QTetris
TOTAL_STATES = 2**20


import random
import numpy as np
import sys
from tqdm import tqdm

def main():

    if len(sys.argv) != 2:
        raise Exception("usage: python3 random-decisio.py <output>.policy")
    # Generate policy and save towards value
    final_p = np.zeros(TOTAL_STATES + 1, dtype=int)
    for i in tqdm(range(len(final_p))):
        final_p[i] = np.random.randint(0, 5)
    np.savetxt(sys.argv[1], final_p, delimiter=',', fmt='%s')
    print("finished!")

if __name__ == '__main__':
    main()
