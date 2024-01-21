from gymnasium.envs.registration import register

from twenty_forty_eight.envs.twenty_forty_eight_env import TwentyFortyEightEnv
from twenty_forty_eight.envs.twenty_forty_eight_model import TwentyFortyEightModel
from twenty_forty_eight.envs.twenty_forty_eight_model import TwentyFortyEightState

register(
    # twenty_forty_eight is this folder name
    # -v0 is because this first version
    # TwentyFortyEight is the pretty name for gym.make
    id="twenty_forty_eight/TwentyFortyEight-v0",
    
    # twenty_forty_eight.envs is the path twenty_forty_eight/envs
    # UniformCoinsEnv is the class name
    entry_point="twenty_forty_eight.envs:TwentyFortyEightEnv",
    
    # configure the automatic wrapper to truncate after 50 steps
    max_episode_steps=100_000,
)
