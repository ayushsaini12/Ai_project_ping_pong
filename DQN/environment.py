import pygame
import numpy as np

class PongGame:
    def _init_(self):
        # Initialize Pygame and set up the game window
        pygame.init()
        self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Pong AI')

        # Game variables
        self.paddle_width, self.paddle_height = 60, 10
        self.ball_radius = 7
        self.paddle_speed = 6
        self.ball_speed_x = 3 * np.random.choice([-1, 1])
        self.ball_speed_y = 3 * np.random.choice([-1, 1])
        self.player_paddle_y = self.height - self.paddle_height - 10

        # Initialize state
        self.reset()

    def reset(self):
        # Reset the game state
        self.player_paddle_x = self.width // 2 - self.paddle_width // 2
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        return np.array([self.ball_x, self.ball_y, self.ball_speed_x, self.ball_speed_y])

    def step(self, action):
        # Apply action
        if action == 0:  # Move left
            self.player_paddle_x -= self.paddle_speed
        elif action == 2:  # Move right
            self.player_paddle_x += self.paddle_speed

        # Keep paddle within screen
        self.player_paddle_x = max(0, min(self.width - self.paddle_width, self.player_paddle_x))

        # Update ball position
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        # Ball collision with walls
        if self.ball_x < 0 or self.ball_x > self.width:
            self.ball_speed_x *= -1
        if self.ball_y < 0:
            self.ball_speed_y *= -1

        # Ball collision with paddle
        if self.player_paddle_y < self.ball_y + self.ball_radius < self.player_paddle_y + self.paddle_height and \
           self.player_paddle_x < self.ball_x < self.player_paddle_x + self.paddle_width:
            self.ball_speed_y *= -1

        # Check if ball is out of bounds
        done = self.ball_y > self.height

        # Compute reward
        reward = 1 if self.ball_y < self.height else -10

        # Return next state, reward, and done
        next_state = np.array([self.ball_x, self.ball_y, self.ball_speed_x, self.ball_speed_y])
        return next_state, reward, done

    def render(self):
        # Render the game state
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.player_paddle_x, self.player_paddle_y, self.paddle_width, self.paddle_height))
        pygame.draw.circle(self.screen, (255, 255, 255), (int(self.ball_x), int(self.ball_y)), self.ball_radius)
        pygame.display.flip()

    def close(self):
        pygame.quit()