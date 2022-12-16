import random
from zlib import decompressobj
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer
import math
import copy

class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        # Do the rest of your implementation here

    def update_board(self, state:Tuple[np.array, Dict[int, Integer]],column: int, player_num: int, is_popout: bool):
        board = state[0]
        num_popouts = state[1]
        if not is_popout:
            if 0 in board[:, column]:
                for row in range(1, board.shape[0]):
                    update_row = -1
                    if board[row, column] > 0 and board[row - 1, column] == 0:
                        update_row = row - 1
                    elif row == board.shape[0] - 1 and board[row, column] == 0:
                        update_row = row
                    if update_row >= 0:
                        board[update_row, column] = player_num
                        # self.c.itemconfig(self.gui_board[column][update_row], fill=self.colors[self.current_turn + 1])
                        break
            # else:
                # err = 'Invalid move by player {}. Column {}'.format(player_num, column, is_popout)
                # raise Exception(err)
        else:
            if 1 in board[:, column] or 2 in board[:, column]:
                for r in range(board.shape[0] - 1, 0, -1):
                    board[r, column] = board[r - 1, column]
                    # self.c.itemconfig(self.gui_board[column][r], fill=self.colors[
                        # board[r, column]])  # this needs to be tweaked
                board[0, column] = 0
                # self.c.itemconfig(self.gui_board[column][0], fill=self.colors[0])
            # else:
                # err = 'Invalid move by player {}. Column {}'.format(player_num, column)
                # raise Exception(err)
            num_popouts[player_num].decrement()
        state = (board,num_popouts)

    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        depth =2
        new_state = copy.deepcopy(state)
        valid_actions= get_valid_actions(self.player_number,new_state)
        # if(len(valid_actions)>=14):
        #     depth = 1
        # if(len(valid_actions)>=14):
        #     depth = 3
        # elif(len(valid_actions)>=12):
        #     depth = 3
        # elif (len(valid_actions)>=8):
        #     depth = 4
        # elif(len(valid_actions)>5):
        #     depth = 5
        # elif(len(valid_actions)<=5):
        #     depth = 6
        if(len(valid_actions)>=17):
            depth =2
        elif(len(valid_actions)>=10):
            depth =3
        elif(len(valid_actions)>=7):
            depth = 4
        else:
            depth = 5
        answer = self.maxi(state, depth, -math.inf, math.inf)
        return answer[1]

        raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        depth =4
        new_state = copy.deepcopy(state)
        valid_actions= get_valid_actions(self.player_number,new_state)
        # if(len(valid_actions)>=14):
        #     depth = 1
        # elif(len(valid_actions)>=12):
        #     depth = 2
        if(len(valid_actions)>=17):
            depth =2
        elif(len(valid_actions)>=10):
            depth =3
        elif(len(valid_actions)>=7):
            depth = 4
        else:
            depth = 5
        answer = self.expecti(state, depth)
        return answer[1]

        raise NotImplementedError('Whoops I don\'t know what to do')

    def eval(self,player_num, state: Tuple[np.array, Dict[int, Integer]]):
        w1 = 30
        w2 = 3
        w3 = -10
        w4 = 10 
        arr = copy.deepcopy(state[0])
        num_popouts = copy.deepcopy(state[1])
        if(player_num==1):
            player2 = 2
        else:
            player2 = 1
        p1_popouts =num_popouts[player_num]
        p2_popouts =num_popouts[player2]
        count = 0
        l =[]
        for i in range(0,arr.shape[0]):
            si = arr.shape[1]//2
            # l.append((i,si))
            if arr[i,si]==player_num:
                count = count + 1 
            if(si>=1):
                # l.append((i,si-1))
                if arr[i,si-1]==player_num:
                    count = count + 1 
            if(si<arr.shape[1]-1):
                # l.append((i,si+1))
                if arr[i,si+1]==player_num:
                    count = count + 1 
        for i in range(0,arr.shape[1]):
            si = arr.shape[0]//2
            # l.append((i,si))
            if arr[si,i]==player_num:
                count = count + 1 
            if(si>=1):
                # l.append((i,si-1))
                if arr[si-1,i]==player_num:
                    count = count + 1 
            if(si<arr.shape[0]-1):
                # l.append((i,si+1))
                if arr[si+1,i]==player_num:
                    count = count + 1 
        m, n = arr.shape
        count_4 = 0
        final_count_4=0
        # for k in range(n + m - 1):
        #     diag1 = []
        #     diag2 = []
        #     for j in range(max(0, k - m + 1), min(n, k + 1)):
        #         i = k - j
        #         diag1.append(arr[i, j])
        #     for x in range(max(0, k - m + 1), min(n, k + 1)):
        #         j = n - 1 - x
        #         i = k - x
        #         diag2.append(arr[i][j])
        #     for j in range(max(0, k - m + 1), min(n, k + 1)):
        #         i = k - j
        #         diag1.append(arr[i, j])
        #     for i in range(0,arr.shape[0]):
        #         row = arr[i]
        #         n = len(row)
        #         j =0
        #         while j < n:
        #             if row[j] == player2:
        #                 while j < n and row[j] == player2:
        #                     count_4 += 1
        #                     j += 1
        #             else:
        #                 j += 1
        #         if(count_4>=4):
        #             final_count_4 +=1
        #     for i in range(0,arr.shape[1]):
        #         row = arr[:,i]
        #         n = len(row)
        #         j=0
        #         while j < n:
        #             if row[j] == player2:
        #                 while j < n and row[j] == player2:
        #                     count_4 += 1
        #                     j += 1
        #             else:
        #                 j += 1
        #         if(count_4>=4):
        #             final_count_4 +=1
        #     for i in range(0,len(diag1)):
        #         n = len(diag1)
        #         j=0
        #         while j < n:
        #             if diag1[j] == player2:
        #                 while j < n and diag1[j] == player2:
        #                     count_4 += 1
        #                     j += 1
        #             else:
        #                 j += 1
        #         if(count_4>=4):
        #             final_count_4 +=1
        #     for i in range(0,len(diag2)):
        #         # row = arr[:,i]
        #         n = len(diag2)
        #         j=0
        #         while j < n:
        #             if diag2[j] == player2:
        #                 while j < n and diag2[j] == player2:
        #                     count_4 += 1
        #                     j += 1
        #             else:
        #                 j += 1
        #         if(count_4>=4):
        #             final_count_4 +=1
            
        # ans = (w1*count) + (w2*get_pts(player_num,arr)) + (w4*final_count_4)
        ans = (w1*count) + (w2*get_pts(player_num,arr)) + (w4*num_popouts[player_num].get_int())
        return ans

    def evaluation(self, state: Tuple[np.array, Dict[int, Integer]]):  
        opp_number= 2
        if(self.player_number == 1):
            opp_number=2
        else:
            opp_number=1
        number = self.eval(self.player_number, state) - self.eval(opp_number, state)
        return number #number is the score difference

    def mini(self, state: Tuple[np.array, Dict[int, Integer]], depth, a, b) -> Tuple[int, Tuple[int, bool]]:
        if depth ==0:
            return (self.evaluation(state), None)
        else:
            opp_number= 2
            if(self.player_number == 1):
                opp_number=2
            else:
                opp_number=1
            v = math.inf
            neigh = get_valid_actions(opp_number, state)
            if len(neigh) == 0:
                return (self.evaluation(state), None)
            for i in neigh:
                action,is_popout = i
                new_state = copy.deepcopy(state)
                self.update_board(new_state,action,opp_number,is_popout)
                v2 = self.maxi(new_state, depth-1, a, b)
                # v2 = self.maxi(self.getstate(state, i, self.opp_number), depth+1, a, b)
                if v2[0] < v:
                    v = v2[0]
                    move = i
                    b = min(b, v)
                if v <= a:
                    return (v, move)
            return (v, move)

    def maxi(self, state: Tuple[np.array, Dict[int, Integer]], depth, a, b) -> Tuple[int, Tuple[int, bool]]:
        if depth == 0:
            return (self.evaluation(state), None)
        else:
            v = -math.inf
            neigh = get_valid_actions(self.player_number, state)
            if len(neigh) == 0:
                return (self.evaluation(state), None)
            for i in neigh:
                action,is_popout = i
                new_state = copy.deepcopy(state)
                self.update_board(new_state,action,self.player_number,is_popout)
                v1 = self.mini(new_state, depth-1, a, b)
                # v1 = self.mini(self.getstate(state, i, self.player_number), depth+1, a, b)
                if v1[0] > v:
                    v = v1[0]
                    move = i
                    a = max(a, v)
                if v >= b:
                    return (v, move)
            return (v, move)

    def expecti(self, state: Tuple[np.array, Dict[int, Integer]], depth) -> Tuple[int, Tuple[int, bool]]:
        if depth == 0:
            return (self.evaluation(state), None)
        else:
            v = -math.inf
            neigh = get_valid_actions(self.player_number, state)
            if len(neigh) == 0:
                return (self.evaluation(state), None)
            for i in neigh:
                action,is_popout = i
                new_state = copy.deepcopy(state)
                self.update_board(new_state,action,self.player_number,is_popout)
                v1 = self.averageofnext(new_state, depth-1)
                if v1 > v:
                    v = v1
                    move = i
            return (v, move)
    
    def averageofnext(self, state: Tuple[np.array, Dict[int, Integer]], depth) -> int:
        if depth == 0:
            return self.evaluation(state)
        else:
            opp_number= 2
            if(self.player_number == 1):
                opp_number=2
            else:
                opp_number=1
            neigh = get_valid_actions(opp_number, state)
            if len(neigh) == 0:
                return self.evaluation(state)
            noofneigh = len(neigh)
            sum = 0
            for i in neigh:
                action,is_popout = i
                new_state = copy.deepcopy(state)
                self.update_board(new_state,action,opp_number,is_popout)
                v1 = self.expecti(new_state, depth-1)
                sum = sum + v1[0]
        return (sum/noofneigh)

    def getstate(self, state: Tuple[np.array, Dict[int, Integer]], move: Tuple[int, bool], playernumber: int) -> Tuple[np.array, Dict[int, Integer]]:
        (m, n) = state[0].shape
        col = move[0]
        array_new = copy.deepcopy(state[0])
        dict_new = copy.deepcopy(state[1])
        if move[1]==False:
            i=0
            while state[0][i][col]!=0:
                i = i+1
            array_new[i][col]=playernumber
        else:
            for i in range(m-1,1, -1):
                array_new[i][col] = state[0][i-1][col]
            array_new[0][col] = 0
            dict_new[playernumber].decrement()
        return (array_new, dict_new)

