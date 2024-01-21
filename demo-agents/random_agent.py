#!/usr/bin/env python3
import gymnasium as gym
import twenty_forty_eight
import random

def agent_function(state):
    """
    state: A twenty_forty_eight.UniformCoinsState object. The current state of the environment.
    
    returns: An integer, the coin to turn over.
    """
    action = random.choice(twenty_forty_eight.TwentyFortyEightModel.ACTIONS(state))
    return action

def main():
    #render_mode = None
#    render_mode = "ansi"
    # render_mode = "rgb_array"
    render_mode = "human"

    env = gym.make('twenty_forty_eight/TwentyFortyEight-v0', render_mode=render_mode)
    observation, info = env.reset()
    state = twenty_forty_eight.TwentyFortyEightState()
    state.observation = observation
    
    terminated = truncated = False
    if render_mode == "ansi":
        print("Current state:", env.render())
    while not (terminated or truncated):
        action = agent_function(state)
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
    

