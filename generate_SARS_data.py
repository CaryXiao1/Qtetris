import numpy as np
import copy
import time
from collections import deque

from engine.miniplayerboard import MiniPlayerBoard
from engine.mini_tetromino_utils import *

def dummy_test():
    b = MiniPlayerBoard()
    print(b.get_state())
    b.cur_type = 'L'
    b.piece_ori = get_start_ori('L')
    print(b.get_state())
    b.cur_type = 'I'
    b.piece_ori = get_start_ori('I')
    print(b.get_state())
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

        seen_states.add(2107640)
        seen_states.add(100488)
        q.append(2107640)
        q.append(100488)


        while q:

            state = q.popleft()

            for a in range(5):  # try all actions
                b = MiniPlayerBoard(state)
                b.set_move(a)
                '''print('statrting with', b.get_state(), a)
                while b.get_state() == state:
                    r = b.turn(regen=False)
                    print(r, b.get_state())
                print('escaped')'''

                r = b.turn(regen=False)
                next_state = b.get_state()

                if r == -100:  # game over
                    if not (state, a, next_state) in written_state_action_next:
                        f.write(str(state)+','+str(a)+','+str(r)+','+str(next_state)+'\n')
                        written_state_action_next.add((state, a, next_state))
                elif b.hit_bottom or r != 0:
                    for possible_type in ['L', 'I']:
                        b.cur_type = possible_type
                        b.piece_ori = get_start_ori(possible_type)
                        (b.piece_r, b.piece_c) = (0, 1)
                        b.ori_number = 0
                        next_state = b.get_state()
                        if b.check_collision(b.piece_ori, b.piece_r, b.piece_c, len(b.piece_ori)):
                            if not (state, a, next_state) in written_state_action_next:
                                f.write(str(state)+','+str(a)+','+str(r-100)+','+str(next_state)+'\n')
                                written_state_action_next.add((state, a, next_state))
                        else:
                            if not (state, a, next_state) in written_state_action_next:
                                f.write(str(state)+','+str(a)+','+str(r)+','+str(next_state)+'\n')
                                written_state_action_next.add((state, a, next_state))
                            if not next_state in seen_states:
                                q.append(next_state)
                                seen_states.add(next_state)
                else:  # no lines cleared
                    if not (state, a, next_state) in written_state_action_next:
                        f.write(str(state)+','+str(a)+','+str(r)+','+str(next_state)+'\n')
                        written_state_action_next.add((state, a, next_state))
                    if not next_state in seen_states:
                        q.append(next_state)
                        seen_states.add(next_state)

if __name__ == '__main__':
    main()
