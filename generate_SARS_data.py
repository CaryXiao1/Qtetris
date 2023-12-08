import numpy as np
import copy
from tqdm import tqdm
from collections import deque

from engine.miniplayerboard import MiniPlayerBoard
from engine.mini_tetromino_utils import *

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

        temps = b.get_state()
        while b.get_state() == temps: b = MiniPlayerBoard()

        seen_states.add(b.get_state())
        q.append(b.get_state())

        p_bar = tqdm(total=437400)
        p_bar.update()

        while q:

            p_bar.update()

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
    p_bar.close()

if __name__ == '__main__':
    main()
