import numpy as np
import copy
from tqdm import tqdm
from collections import deque

from engine.miniplayerboard import MiniPlayerBoard
from engine.mini_tetromino_utils import *

def get_start_states():  # should print 2197640, 100488
    b = MiniPlayerBoard()
    state = b.get_state()
    print(state)
    while state == b.get_state(): b = MiniPlayerBoard()
    print(b.get_state())

def goofyahhhtest():
    b1 = MiniPlayerBoard()
    state1 = b1.get_state()
    print(state1)
    b2 = MiniPlayerBoard(state1)
    state2 = b2.get_state()
    print(state2)
    assert state1 == state2
    b2.turn()
    state3 = b2.get_state()
    print(state3)
    b2.turn()
    print(b2.get_state())
    b2.turn()
    print(b2.get_state())
    b2.turn()
    print(b2.get_state())
    b2.turn()
    print(b2.get_state())
    return

"""
This function creates outfile.txt with the list of ~5million
tuples (state, action, reward, state'), for all possible
state-action pairs in the miniboard game
"""
def main():
    with open ('outfile.csv', 'x') as f:
        q = deque()
        seen_states = set()
        written_state_action_next = set()

        b = MiniPlayerBoard()

        seen_states.add(b.get_state())
        q.append(b.get_state())

        counter = 0

        while q:

            if counter % 10000 == 0:  # progress print
                print(str(counter) + ' / ~10,000,000')
            counter += 1

            state = q.popleft()

            for a in range(5):  # try all actions
                b = MiniPlayerBoard(state)
                b.set_move(a)
                while b.get_state() == state: r = b.turn()
                next_state = b.get_state()

                if r == -100:  # game over
                    if not (state, a, next_state) in written_state_action_next:
                        f.write(str(state)+','+str(a)+','+str(r)+','+str(next_state)+'\n')
                        written_state_action_next.add((state, a, next_state))
                elif r == 0:  # no lines cleared
                    if not (state, a, next_state) in written_state_action_next:
                        f.write(str(state)+','+str(a)+','+str(r)+','+str(next_state)+'\n')
                        written_state_action_next.add((state, a, next_state))
                    if not next_state in seen_states:
                        q.append(next_state)
                        seen_states.add(next_state)
                else:  # some lines cleared
                    for possible_type in ['L', 'I']:
                        b.cur_type = possible_type
                        b.piece_ori = get_start_ori(possible_type)
                        next_state = b.get_state()
                        if b.check_collision(b.piece_ori, b.piece_r, b.piece_c, len(b.piece_ori)):
                            if not (state, a, next_state) in written_state_action_next:
                                f.write(str(state)+','+str(a)+','+str(r)+','+str(next_state)+'\n')
                                written_state_action_next.add((state, a, next_state))
                        else:
                            if not (state, a, next_state) in written_state_action_next:
                                f.write(str(state)+','+str(a)+','+str(r)+','+str(next_state)+'\n')
                                written_state_action_next.add((state, a, next_state))
                            if not next_state in seen_states:
                                q.append(next_state)
                                seen_states.add(next_state)

if __name__ == '__main__':
    main()
