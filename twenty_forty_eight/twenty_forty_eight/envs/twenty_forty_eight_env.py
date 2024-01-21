import gymnasium
import math
import random
import numpy as np
from gymnasium import spaces
from twenty_forty_eight.envs.twenty_forty_eight_model import TwentyFortyEightModel
from twenty_forty_eight.envs.twenty_forty_eight_model import TwentyFortyEightState

try:
    import pygame
except ImportError as e:
    raise DependencyNotInstalled(
        "pygame is not installed, `pip install` must have failed."
    ) from e

class TwentyFortyEightEnv(gymnasium.Env):

    metadata = {
        "render_modes": ["human", "ansi"],
        "render_fps": 10,
    }

    def __init__(self, render_mode=None):
        self.render_mode = render_mode
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(0, 1024, shape=(4,4), dtype=np.int16)
        self.size = 16
        self.rows = 4
        self.cols = 4

        # display support
        self.gap = self.rows*2
        if (render_mode == "human"):
            self.color_dictionary = { 
                                     0: (190, 190, 190),
                                     2: (31, 81, 255),
                                     4: (255, 87, 51),
                                     8: (57, 255, 20),
                                     16: (255, 0, 0)}
            pygame.font.init()
            self.font = pygame.font.SysFont('Clear Sans', 50, bold=True, italic=False)
            self.text_color = (255,255,255)
        self.cell_size = (800//math.floor(self.size**0.5)) - self.gap
        self.window_size = (
            math.floor(self.size**0.5) * self.cell_size + self.gap,
            math.floor(self.size**0.5) * self.cell_size + self.gap,
        )
        self.window_surface = None
        self.clock = None
        self.background_color = (170, 170, 170)
        return

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = TwentyFortyEightState()
        self.state.reset()

        observation = self.state.observation
        info = {}
        return observation, info

    def step(self, action):
        state = self.state
        state1 = TwentyFortyEightModel.RESULT(state, action)
        self.state = state1
        
        observation = self.state.observation
        reward = TwentyFortyEightModel.STEP_COST(state, action, state1)
        terminated = TwentyFortyEightModel.GAME_OVER(state1)
        info = {}

        # display support
        if self.render_mode == "human":
            self.render(action)
        return observation, reward, terminated, False, info

    def render(self, action=None):
        if self.render_mode is None:
            assert self.spec is not None
            gym.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym.make("{self.spec.id}", render_mode="ansi")'
            )
            return

        if self.render_mode == "ansi":
            return self._render_text()
        else:
            return self._render_gui(self.render_mode, action)

    def _render_text(self):
        return str(self.state)

    def _display_board(self):
        rect = pygame.Rect((0,0), self.window_size)
        pygame.draw.rect(self.window_surface, self.background_color, rect)
        for row in range(self.rows):
            for col in range(self.cols):
                x = self.gap + col * self.cell_size
                y = self.gap + row * self.cell_size
                rect = pygame.Rect((x, y), (self.cell_size - self.gap, self.cell_size - self.gap))
                if self.state._board[row][col] not in self.color_dictionary:
                    self.color_dictionary[self.state._board[row][col]] = (random.randrange(255), random.randrange(255), random.randrange(255))
                color = self.color_dictionary[self.state._board[row][col]]
                pygame.draw.rect(self.window_surface, color, rect)
                if self.state._board[row][col] != 0:
                    text_surface_object = self.font.render(str(self.state._board[row][col]), True, self.text_color)
                    text_rect = text_surface_object.get_rect(center=rect.center)
                    self.window_surface.blit(text_surface_object, text_rect)

    def _render_gui(self, mode, action):
        if self.window_surface is None:
            pygame.init()

            if mode == "human":
                pygame.display.init()
                pygame.display.set_caption("Twenty Forty Eight")
                self.window_surface = pygame.display.set_mode(self.window_size)
            else:  # rgb_array
                self.window_surface = pygame.Surface(self.window_size)
        if self.clock is None:
            self.clock = pygame.time.Clock()

        rect = pygame.Rect((0,0), self.window_size)
        pygame.draw.rect(self.window_surface, self.background_color, rect)
        self._display_board()
        arrow = pygame.Surface((300, 300), pygame.SRCALPHA, )
        pygame.draw.polygon(arrow, (255, 255, 255), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))
        arrow = pygame.transform.scale(arrow, (self.window_size[0] // 2, self.window_size[1] // 2))
        arrow = pygame.transform.rotate(arrow, 90.0)
        arrow = pygame.transform.rotate(arrow, -90.0 * action)
        arrow.set_alpha(128) 
        self.window_surface.blit(arrow, (self.window_size[0] // 4, self.window_size[1] // 4)) 
        if mode == "human":
            pygame.event.pump()
            pygame.display.update()
            pygame.time.wait(150)
            self._display_board()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
    def close(self):
        if self.window_surface is not None:
            pygame.display.quit()
            pygame.quit()
        return
    


    
