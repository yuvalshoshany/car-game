import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
ROAD_GRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
PURPLE = (128, 0, 128)

# Car dimensions
CAR_WIDTH = 40
CAR_HEIGHT = 80

# Parking spot dimensions
PARKING_WIDTH = 60
PARKING_HEIGHT = 100

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.acceleration = 0.3
        self.max_speed = 4
        self.turn_speed = 3
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.friction = 0.98  # Add friction to make movement more realistic

    def move(self):
        # Convert angle to radians
        rad = math.radians(self.angle)
        
        # Calculate movement based on angle and speed
        # Note: In pygame, y-axis is inverted (0 is top)
        self.x -= math.sin(rad) * self.speed
        self.y -= math.cos(rad) * self.speed
        
        # Apply friction
        self.speed *= self.friction
        
        # Keep car within screen bounds
        self.x = max(0, min(self.x, WINDOW_WIDTH))
        self.y = max(0, min(self.y, WINDOW_HEIGHT))

    def rotate(self, direction):
        # Allow turning even when stationary
        self.angle += direction * self.turn_speed
        self.angle %= 360

    def accelerate(self):
        self.speed = min(self.speed + self.acceleration, self.max_speed)

    def brake(self):
        self.speed = max(self.speed - self.acceleration, -self.max_speed/2)

    def draw(self, screen):
        # Create a surface for the car
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw car body (main rectangle)
        pygame.draw.rect(car_surface, BLUE, (0, 0, self.width, self.height))
        
        # Draw car roof (slightly smaller rectangle on top)
        roof_width = self.width * 0.8
        roof_height = self.height * 0.4
        roof_x = (self.width - roof_width) / 2
        roof_y = self.height * 0.1
        pygame.draw.rect(car_surface, BLUE, (roof_x, roof_y, roof_width, roof_height))
        
        # Draw windows
        window_width = self.width * 0.6
        window_height = self.height * 0.25
        window_x = (self.width - window_width) / 2
        window_y = self.height * 0.15
        pygame.draw.rect(car_surface, GRAY, (window_x, window_y, window_width, window_height))
        
        # Draw headlights
        headlight_width = self.width * 0.15
        headlight_height = self.height * 0.1
        # Front headlights
        pygame.draw.rect(car_surface, YELLOW, (0, 0, headlight_width, headlight_height))
        pygame.draw.rect(car_surface, YELLOW, (self.width - headlight_width, 0, headlight_width, headlight_height))
        
        # Draw wheels
        wheel_width = self.width * 0.25
        wheel_height = self.height * 0.2
        # Front wheels
        pygame.draw.rect(car_surface, BLACK, (0, 0, wheel_width, wheel_height))
        pygame.draw.rect(car_surface, BLACK, (self.width - wheel_width, 0, wheel_width, wheel_height))
        # Back wheels
        pygame.draw.rect(car_surface, BLACK, (0, self.height - wheel_height, wheel_width, wheel_height))
        pygame.draw.rect(car_surface, BLACK, (self.width - wheel_width, self.height - wheel_height, wheel_width, wheel_height))
        
        # Draw wheel rims
        rim_width = wheel_width * 0.6
        rim_height = wheel_height * 0.6
        # Front rims
        pygame.draw.rect(car_surface, GRAY, (wheel_width * 0.2, wheel_height * 0.2, rim_width, rim_height))
        pygame.draw.rect(car_surface, GRAY, (self.width - wheel_width + wheel_width * 0.2, wheel_height * 0.2, rim_width, rim_height))
        # Back rims
        pygame.draw.rect(car_surface, GRAY, (wheel_width * 0.2, self.height - wheel_height + wheel_height * 0.2, rim_width, rim_height))
        pygame.draw.rect(car_surface, GRAY, (self.width - wheel_width + wheel_width * 0.2, self.height - wheel_height + wheel_height * 0.2, rim_width, rim_height))
        
        # Rotate the car
        rotated_car = pygame.transform.rotate(car_surface, self.angle)
        
        # Get the rect for drawing
        car_rect = rotated_car.get_rect(center=(self.x, self.y))
        
        # Draw the car
        screen.blit(rotated_car, car_rect)
        return car_rect

    def get_car_rect(self):
        # Create a surface for collision detection
        car_surface = pygame.Surface((self.width, self.height))
        car_surface.fill(BLUE)
        
        # Rotate the car
        rotated_car = pygame.transform.rotate(car_surface, self.angle)
        
        # Return the rect for collision detection
        return rotated_car.get_rect(center=(self.x, self.y))

class ParkingSpot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PARKING_WIDTH
        self.height = PARKING_HEIGHT
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen):
        # Draw parking spot with dashed lines
        pygame.draw.rect(screen, GREEN, self.rect, 2)
        # Draw dashed lines
        dash_length = 10
        dash_space = 5
        for i in range(0, self.width, dash_length + dash_space):
            pygame.draw.line(screen, GREEN, (self.x + i, self.y), 
                           (self.x + min(i + dash_length, self.width), self.y), 2)

class ObstacleCar:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = CAR_HEIGHT  # Swap width and height for horizontal orientation
        self.height = CAR_WIDTH
        self.speed = random.uniform(2, 4)  # Random speed between 2 and 4
        self.direction = 1  # 1 for right, -1 for left

    def move(self):
        # Move the car
        self.x += self.speed * self.direction
        
        # Change direction when reaching screen edges with some padding
        if self.x <= 50 or self.x >= WINDOW_WIDTH - self.width - 50:
            self.direction *= -1
            # Ensure car doesn't get stuck in wall
            self.x = max(50, min(self.x, WINDOW_WIDTH - self.width - 50))

    def draw(self, screen):
        # Create a surface for the car
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw car body (main rectangle)
        pygame.draw.rect(car_surface, self.color, (0, 0, self.width, self.height))
        
        # Draw car roof (slightly smaller rectangle on top)
        roof_width = self.width * 0.4  # Adjusted for horizontal orientation
        roof_height = self.height * 0.8
        roof_x = self.width * 0.1
        roof_y = (self.height - roof_height) / 2
        pygame.draw.rect(car_surface, self.color, (roof_x, roof_y, roof_width, roof_height))
        
        # Draw windows
        window_width = self.width * 0.25
        window_height = self.height * 0.6
        window_x = self.width * 0.15
        window_y = (self.height - window_height) / 2
        pygame.draw.rect(car_surface, GRAY, (window_x, window_y, window_width, window_height))
        
        # Draw headlights
        headlight_width = self.height * 0.15
        headlight_height = self.height * 0.1
        # Front headlights
        pygame.draw.rect(car_surface, YELLOW, (0, (self.height - headlight_height) / 2, headlight_width, headlight_height))
        pygame.draw.rect(car_surface, YELLOW, (self.width - headlight_width, (self.height - headlight_height) / 2, headlight_width, headlight_height))
        
        # Draw wheels
        wheel_width = self.height * 0.25
        wheel_height = self.height * 0.2
        # Front wheels
        pygame.draw.rect(car_surface, BLACK, (0, 0, wheel_width, wheel_height))
        pygame.draw.rect(car_surface, BLACK, (0, self.height - wheel_height, wheel_width, wheel_height))
        # Back wheels
        pygame.draw.rect(car_surface, BLACK, (self.width - wheel_width, 0, wheel_width, wheel_height))
        pygame.draw.rect(car_surface, BLACK, (self.width - wheel_width, self.height - wheel_height, wheel_width, wheel_height))
        
        # Draw wheel rims
        rim_width = wheel_width * 0.6
        rim_height = wheel_height * 0.6
        # Front rims
        pygame.draw.rect(car_surface, GRAY, (wheel_width * 0.2, wheel_height * 0.2, rim_width, rim_height))
        pygame.draw.rect(car_surface, GRAY, (wheel_width * 0.2, self.height - wheel_height + wheel_height * 0.2, rim_width, rim_height))
        # Back rims
        pygame.draw.rect(car_surface, GRAY, (self.width - wheel_width + wheel_width * 0.2, wheel_height * 0.2, rim_width, rim_height))
        pygame.draw.rect(car_surface, GRAY, (self.width - wheel_width + wheel_width * 0.2, self.height - wheel_height + wheel_height * 0.2, rim_width, rim_height))
        
        # Draw the car
        screen.blit(car_surface, (self.x, self.y))
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Car Parking Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.reset_game()

    def reset_game(self):
        # Initialize car at bottom center
        self.car = Car(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100)
        
        # Initialize parking spot at top center
        self.parking_spot = ParkingSpot(WINDOW_WIDTH // 2 - PARKING_WIDTH // 2, 50)
        
        # Initialize obstacles
        self.obstacles = []
        self.generate_obstacles()
        
        self.game_over = False

    def generate_obstacles(self):
        self.obstacles = []
        # Generate 3-4 random obstacle cars
        obstacle_colors = [BROWN, YELLOW, GREEN, PURPLE]
        for _ in range(random.randint(3, 4)):
            attempts = 0
            while attempts < 100:  # Limit attempts to prevent infinite loop
                # Spawn cars away from walls
                x = random.randint(100, WINDOW_WIDTH - CAR_HEIGHT - 100)
                y = random.randint(150, WINDOW_HEIGHT - 100)  # Start below parking spot
                color = random.choice(obstacle_colors)
                obstacle = ObstacleCar(x, y, color)
                
                # Check if obstacle overlaps with parking spot, car, or other obstacles
                if not obstacle.get_rect().colliderect(self.parking_spot.rect):
                    # Check car collision
                    car_rect = self.car.get_car_rect()
                    if not obstacle.get_rect().colliderect(car_rect):
                        overlap = False
                        for existing_obstacle in self.obstacles:
                            if obstacle.get_rect().colliderect(existing_obstacle.get_rect()):
                                overlap = True
                                break
                        if not overlap:
                            self.obstacles.append(obstacle)
                            break
                attempts += 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.score = 0
                    self.reset_game()

        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.car.rotate(1)
        if keys[pygame.K_RIGHT]:
            self.car.rotate(-1)
        if keys[pygame.K_UP]:
            self.car.accelerate()
        if keys[pygame.K_DOWN]:
            self.car.brake()

    def check_collisions(self):
        car_rect = self.car.get_car_rect()
        
        # Check collision with obstacles
        for obstacle in self.obstacles:
            if car_rect.colliderect(obstacle.get_rect()):
                self.game_over = True
                return
        
        # Check if car is parked correctly
        if car_rect.colliderect(self.parking_spot.rect):
            # Check if car is roughly parallel to parking spot
            if abs(self.car.angle) < 10 or abs(self.car.angle - 360) < 10:
                self.score += 1
                self.reset_game()

    def draw(self):
        # Draw road background
        self.screen.fill(ROAD_GRAY)
        
        # Draw road lines (dashed lines)
        dash_length = 30
        dash_space = 40
        for i in range(0, WINDOW_WIDTH, dash_length + dash_space):
            pygame.draw.line(self.screen, WHITE, (i, WINDOW_HEIGHT // 2), 
                           (min(i + dash_length, WINDOW_WIDTH), WINDOW_HEIGHT // 2), 3)
        
        # Draw side lines
        pygame.draw.line(self.screen, WHITE, (0, 0), (0, WINDOW_HEIGHT), 5)
        pygame.draw.line(self.screen, WHITE, (WINDOW_WIDTH, 0), (WINDOW_WIDTH, WINDOW_HEIGHT), 5)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw parking spot
        self.parking_spot.draw(self.screen)
        
        # Draw car
        self.car.draw(self.screen)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = font.render("Game Over! Press R to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            
            if not self.game_over:
                self.car.move()
                # Move obstacles
                for obstacle in self.obstacles:
                    obstacle.move()
                self.check_collisions()
            
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run() 