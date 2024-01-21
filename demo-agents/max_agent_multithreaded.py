#!/usr/bin/env python3
from multiprocessing import Process, Array
import gymnasium as gym
import twenty_forty_eight
import copy
import numpy as np
import time

INFINITY = 1_000_000
def MAXMAX(state, depth, model, evaluations, thread):
    if depth == 0 or model.GAME_OVER(state):
        return model.EVALUATION(state)
    value = 0
    for a in model.ACTIONS(state):
        result = model.RESULT(state, a)
        if model.EVALUATION(result) <= model.EVALUATION(state):
            continue
        value = max(value, MAXMAX(copy.deepcopy(result), depth - 1, model, evaluations, thread) )
    evaluations[thread] = value
    return value


def agent_function(state, model):
    """
    state: A twenty_forty_eight.TwentyFortyEightState object. The current state of the environment.
    
    returns: An integer, the action to take.
    """
    evaluations = Array('i', [0]*len(model.ACTIONS(state)))
    processes = []
    thread = 0
    possible_actions = model.ACTIONS(state)
    start = time.time()
    for possible_action in possible_actions:
        processes.append(Process(target=MAXMAX, args=(model.RESULT(copy.deepcopy(state), possible_action), 6, model, evaluations, thread)))
        processes[-1].start()
        thread += 1
    for proc in processes:
        proc.join()
    print(list(evaluations))
    best_action = [-INFINITY, None]
    same_action = {}
    for i in range(len(evaluations)):
        if evaluations[i] > best_action[0]:
            best_action = [evaluations[i], possible_actions[i]]
            same_action[evaluations[i]] = [possible_actions[i]]
        elif evaluations[i] == best_action[0]:
            same_action[evaluations[i]].append(possible_actions[i])
    if best_action[1] == None:
        best_action[1] = np.random.choice(model.ACTIONS(state))
    elif len(same_action[best_action[0]]) > 1:
        best_action[1] = np.random.choice(same_action[best_action[0]])
    print("Taking action: ", best_action[1], "Time: ", time.time() - start)
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
    

