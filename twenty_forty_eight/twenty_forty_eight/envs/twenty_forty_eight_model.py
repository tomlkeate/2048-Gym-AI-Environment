import numpy as np
import math
import random
import copy

class TwentyFortyEightState:
    """A Game of Twenty Forty Eight."""

    def __init__(self, size=4):
        self._board = np.full((size,size), 0, dtype=np.int16)
        self._size = size * size
        self._rows = size
        self._cols = size
        location1 = (random.randrange(self._rows), random.randrange(self._cols))
        self._board[location1[0], location1[1]] = 2
        self._board[np.random.choice([i for i in range(self._rows) if i != location1[0]]), np.random.choice([i for i in range(self._cols) if i != location1[1]])] = 2
        self._actions = 4
        return

    @property
    def size(self):
        return self._size
    """
    def randomize(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
        self._board = np.random.randint(2, size=self._size, dtype=np.int8)
        return self._board
    """
    def reset(self):
        self._board.fill(0)
        location1 = (random.randrange(self._rows), random.randrange(self._cols))
        self._board[location1[0], location1[1]] = 2
        self._board[np.random.choice([i for i in range(self._rows) if i != location1[0]]), np.random.choice([i for i in range(self._cols) if i != location1[1]])] = 2
        return self._board

    def insert_block(self):
        inserted = False
        for row in reversed(range(self._rows)):
            for col in range(self._cols):
                if self._board[row][col] == 0:
                    inserted = True
                    self._board[row][col] = 2
                    break
            if inserted:
                break

    def turn(self, action):
        """action: direction of game movement
                North
                  0  
           West 3   1 East
                  2
                South"""
        update = False
        if action == 0:
            """ Go North """
            changed = True
            combined = []
            while changed:
                changed = False
                for row in reversed(range(self._rows - 1)): # [2, 1, 0]
                    for col in range(self._cols):
                        if self._board[row][col] == 0 and self._board[row + 1][col] != 0:
                            self._board[row][col] = self._board[row + 1][col]
                            self._board[row + 1][col] = 0
                            changed = True
                            update = True
                        elif self._board[row][col] != 0 and (row, col) not in combined and (row + 1, col) not in combined and self._board[row][col] == self._board[row + 1][col]:
                            self._board[row][col] += self._board[row + 1][col]
                            self._board[row + 1][col] = 0
                            combined.append((row, col))
                            changed = True
                            update = True
        elif action == 1:
            """ Go East """
            changed = True
            combined = []
            while changed:
                changed = False
                for col in range(1, self._cols): # [1, 2, 3]
                    for row in range(self._rows):
                        if self._board[row][col] == 0 and self._board[row][col - 1] != 0:
                            self._board[row][col] = self._board[row][col - 1]
                            self._board[row][col - 1] = 0
                            changed = True
                            update = True
                        elif self._board[row][col] != 0 and (row, col) not in combined and (row, col - 1) not in combined and self._board[row][col] == self._board[row][col - 1]:
                            self._board[row][col] += self._board[row][col - 1]
                            self._board[row][col - 1] = 0
                            combined.append((row, col))
                            changed = True
                            update = True
        elif action == 2:
            """ Go South """
            changed = True
            combined = []
            while changed:
                changed = False
                for row in range(1, self._rows): # [1, 2, 3]
                    for col in range(self._cols):
                        if self._board[row][col] == 0 and self._board[row - 1][col] != 0:
                            self._board[row][col] = self._board[row - 1][col]
                            self._board[row - 1][col] = 0
                            changed = True
                            update = True
                        elif self._board[row][col] != 0 and (row, col) not in combined and (row - 1, col) not in combined and self._board[row][col] == self._board[row - 1][col]:
                            self._board[row][col] += self._board[row - 1][col]
                            self._board[row - 1][col] = 0
                            combined.append((row, col))
                            changed = True
                            update = True
        elif action == 3:
            """ Go West """
            changed = True
            combined = []
            while changed:
                changed = False
                for col in reversed(range(self._cols - 1)): # [2, 1, 0]
                    for row in range(self._rows):
                        if self._board[row][col] == 0 and self._board[row][col + 1] != 0:
                            self._board[row][col] = self._board[row][col + 1]
                            self._board[row][col + 1] = 0
                            changed = True
                            update = True
                        elif self._board[row][col] != 0 and (row, col) not in combined and (row, col + 1) not in combined and self._board[row][col] == self._board[row][col + 1]:
                            self._board[row][col] += self._board[row][col + 1]
                            self._board[row][col + 1] = 0
                            combined.append((row, col))
                            changed = True
                            update = True
        elif not action == None:
            class BadAction(Exception): 
                def __init__(self): ...
            raise BadAction
        if update:
            self.insert_block()
        return

    @property
    def observation(self):
        return self._board

    @observation.setter
    def observation(self, value):
        self._board = value
        self._size = value.shape[0]
        return

    def number(self, row, col):
        return self._board[row][col]

    def __str__(self):
        return "\n " + str(self._board)[1:-1] + "\n"

#if __name__ == "__main__":
#    s = TwentyFortyEightState()
#    while True:
#        s.insert_block()
#        print(s)
#        move = input("Enter Move: ")
#        if move == "n":
#            s.turn(0)
#        elif move == 'e':
#            s.turn(1)
#        elif move == 's':
#            s.turn(2)
#        elif move == 'w':
#            s.turn(3)

class TwentyFortyEightModel:
    def ACTIONS(state):
        actions = [i for i in range(state._actions)]
        if 0 not in state._board:
            actions = []
            for row in range(state._rows):
                for col in range(state._cols - 1):
                    if state._board[row][col] == state._board[row][col + 1]:
                        actions.append(1)
                        actions.append(3)
            for row in range(state._rows - 1):
                for col in range(state._cols):
                    if state._board[row][col] == state._board[row + 1][col]:
                        actions.append(0)
                        actions.append(2)
        return actions

    def RESULT(state, action):
        state1 = copy.deepcopy(state)
        state1.turn(action)
        return state1

    def STEP_COST(state, action, state1):
        return 1

    def EVALUATION(state):
        # Evalutation
        score = 0
        for row in range(state._rows):
            for col in range(state._cols):
                score += math.ceil(state._board[row][col]**1.25)
                if state._board[row][col] == 0:
                    score += 1
        if 0 not in state._board:
            for row in range(state._rows):
                for col in range(state._cols - 1):
                    if state._board[row][col] == state._board[row][col + 1]:
                        return score
            for row in range(state._rows - 1):
                for col in range(state._cols):
                    if state._board[row][col] == state._board[row + 1][col]:
                        return score
            return 0
        return score

    def GAME_OVER(state):
        if 0 not in state._board:
            for row in range(state._rows):
                for col in range(state._cols - 1):
                    if state._board[row][col] == state._board[row][col + 1]:
                        return False
            for row in range(state._rows - 1):
                for col in range(state._cols):
                    if state._board[row][col] == state._board[row + 1][col]:
                        return False
            return True
        return False

if __name__ == "__main__":
    state = TwentyFortyEightState(7)
    actions = TwentyFortyEightModel.ACTIONS(state)
    print(actions)

    state = TwentyFortyEightState(13)
    actions = TwentyFortyEightModel.ACTIONS(state)
    print(actions)

    print()
    state = TwentyFortyEightState(13)
    print(state)
    state1 = TwentyFortyEightModel.RESULT(state, 3)
    print(state1)

    print()
    state = TwentyFortyEightState(13)
    print(TwentyFortyEightModel.GOAL_TEST(state))
    print(TwentyFortyEightModel.GOAL_TEST(state))
    
    print()
    state = TwentyFortyEightState(13)
    print(state)
    action = 2
    state1 = TwentyFortyEightModel.RESULT(state, action)
    print(TwentyFortyEightModel.STEP_COST(state, action, state1))
