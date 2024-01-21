#!/usr/bin/env python3
import gymnasium as gym
import twenty_forty_eight
import copy
import numpy as np

INFINITY = 1_000_000
def MAXMAX(state, depth, model):
    if depth == 0 or model.GAME_OVER(state):
        return model.EVALUATION(state)
    value = -INFINITY
    for a in model.ACTIONS(state):
        result = model.RESULT(state, a)
        if model.EVALUATION(result) <= model.EVALUATION(state) - 1:
            value = model.EVALUATION(result)
            continue
        value = max( value, MAXMAX(copy.deepcopy(result), depth - 1, model) )
    return value if value != -INFINITY else 0


def agent_function(state, model):
    """
    state: A twenty_forty_eight.TwentyFortyEightState object. The current state of the environment.
    
    returns: An integer, the action to take.
    """
    best_action = [0, None]
    same_action = {}
    for possible_action in model.ACTIONS(state):
        evaluation = MAXMAX(model.RESULT(copy.deepcopy(state), possible_action), 4, model)
        print(evaluation)
        if evaluation > best_action[0]:
            best_action = [evaluation, possible_action]
            same_action[evaluation] = [possible_action]
        elif evaluation == best_action[0]:
            same_action[evaluation].append(possible_action)
    if best_action[1] == None:
        best_action[1] = np.random.choice(model.ACTIONS(state))
    elif len(same_action[best_action[0]]) > 1:
        print(same_action[best_action[0]])
        best_action[1] = np.random.choice(same_action[best_action[0]])
    return best_action[1]

def main():
    model = twenty_forty_eight.TwentyFortyEightModel
    # render_mode = None
#    render_mode = "ansi"
    render_mode = "human"

    env = gym.make('twenty_forty_eight/TwentyFortyEight-v0', render_mode=render_mode)
    observation, info = env.reset()
    state = twenty_forty_eight.TwentyFortyEightState()
    state.observation = observation
    
    terminated = truncated = False
    if render_mode == "ansi":
        print("Current state:", env.render())
    while not (terminated or truncated):
        action = agent_function(state, model)
        if action == None:
            break
        if render_mode == "ansi":
            print()
            print(f"Action: {action}.")
        observation, reward, terminated, truncated, info = env.step(action)
        state.observation = observation
        if render_mode == "ansi":
            print("Current state:", env.render())

    env.close()
    return

if __name__ == "__main__":
    main()
    

