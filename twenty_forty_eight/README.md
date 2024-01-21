Twenty Forty Eight Environment
-------------------------

# Description

The state is a 4x4 board of numbers that are powers of 2. 
The goal is to combine cells until you reach 2048.

# Observation Space

An observation is a numpy.array of `int16`, and shape = (N,N).
Each cell has a number associated with it.

# Action Space

An action is an integer representing the cardinal direction
the board should move in.

# Starting State

The starting state is a 4x4 board with two 2's at random locations on the board.

# Rewards

Add up the value of each cell when raised to the power of 5/4.
Add one point for each empty cell.
return zero if no move is available.

# Episode End

The episode terminates when all of the cells have been filled
and there is nothing that can be combined.

The episode will truncate after 100,000 steps. This limit can
be overridden with the `max_episode_steps` parameter to 
`gymnasium.make()`.

