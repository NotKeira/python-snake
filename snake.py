import turtle
import time
import random

# Constants
WIDTH, HEIGHT = 600, 600
DELAY_EASY = 0.15
DELAY_MEDIUM = 0.1
DELAY_HARD = 0.05
FOOD_SIZE = 20
SNAKE_SIZE = 20

# Colors
BG_COLOR = "green"
SNAKE_COLOR = "black"
FOOD_COLOR = "red"
TEXT_COLOR = "white"

class Snake:
    """Represents the snake in the game.

    The snake is controlled by the player and moves around the
    screen, eating food to grow longer.  It can move up, down,
    left, or right.
    """
    def __init__(self):
        """Initialize the snake object."""
        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color(SNAKE_COLOR)
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "stop"
        self.segments = []

    def move(self):
        """Move the snake head."""
        if self.head.direction == "up":
            self.head.sety(self.head.ycor() + SNAKE_SIZE)
        elif self.head.direction == "down":
            self.head.sety(self.head.ycor() - SNAKE_SIZE)
        elif self.head.direction == "left":
            self.head.setx(self.head.xcor() - SNAKE_SIZE)
        elif self.head.direction == "right":
            self.head.setx(self.head.xcor() + SNAKE_SIZE)

    def go_up(self):
        """Set the snake's direction to up."""
        if self.head.direction != "down":
            self.head.direction = "up"

    def go_down(self):
        """Set the snake's direction to down."""
        if self.head.direction != "up":
            self.head.direction = "down"

    def go_left(self):
        """Set the snake's direction to left."""
        if self.head.direction != "right":
            self.head.direction = "left"

    def go_right(self):
        """Set the snake's direction to right."""
        if self.head.direction != "left":
            self.head.direction = "right"

    def grow(self):
        """Add a segment to the snake."""
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        self.segments.append(new_segment)

    def move_body(self):
        """Move the snake's body segments."""
        for index in range(len(self.segments) - 1, 0, -1):
            x = self.segments[index - 1].xcor()
            y = self.segments[index - 1].ycor()
            self.segments[index].goto(x, y)

        if self.segments:
            self.segments[0].goto(self.head.xcor(), self.head.ycor())

    def reset(self):
        """Reset the snake to its initial position and clear segments."""
        self.head.goto(0, 0)
        self.head.direction = "stop"
        for segment in self.segments:
            segment.goto(1000, 1000)
        self.segments.clear()

class Food:
    """Represents the food in the game.

    The food is a circle that the snake eats to grow longer.  It
    appears at random locations on the screen.
    """
    def __init__(self):
        """Initialize the food object."""
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color(FOOD_COLOR)
        self.food.penup()
        self.relocate()

    def relocate(self):
        """Move the food to a random location."""
        x = random.randint(-WIDTH // 2 + FOOD_SIZE, WIDTH // 2 - FOOD_SIZE)
        y = random.randint(-HEIGHT // 2 + FOOD_SIZE, HEIGHT // 2 - FOOD_SIZE)
        self.food.goto(x, y)


# Setup screen
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor(BG_COLOR)
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)  # Turn off screen updates

# Initialize game objects
snake = Snake()
food = Food()

# Score display
pen = turtle.Turtle()
pen.speed(0)
pen.color(TEXT_COLOR)
pen.penup()
pen.hideturtle()
pen.goto(0, HEIGHT // 2 - 40)

# Game variables
score = 0
high_score = 0
delay = DELAY_MEDIUM
paused = False
game_over = False

def update_score_display():
    """Update the score display."""
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Courier", 24, "normal"))

def check_collisions():
    """Check for collisions."""
    global game_over
    if (
        snake.head.xcor() > WIDTH // 2 - SNAKE_SIZE
        or snake.head.xcor() < -WIDTH // 2 + SNAKE_SIZE
        or snake.head.ycor() > HEIGHT // 2 - SNAKE_SIZE
        or snake.head.ycor() < -HEIGHT // 2 + SNAKE_SIZE
    ):
        game_over = True
        return

    for segment in snake.segments:
        if snake.head.distance(segment) < SNAKE_SIZE:
            game_over = True
            return

def check_food_collision():
    """Check for collision with food."""
    global score, delay
    if snake.head.distance(food.food) < FOOD_SIZE:
        food.relocate()
        snake.grow()
        score += 10
        if score > high_score:
            high_score = score
        delay -= 0.001
        update_score_display()


def toggle_pause():
    """Toggle the pause state of the game."""
    global paused, delay
    paused = not paused
    delay = 1 if paused else current_delay


def set_difficulty(difficulty):
    """Set the game difficulty."""
    global delay, current_delay
    if difficulty == "easy":
        delay = DELAY_EASY
    elif difficulty == "medium":
        delay = DELAY_MEDIUM
    elif difficulty == "hard":
        delay = DELAY_HARD
    current_delay = delay


def game_loop():
    """Main game loop."""
    global game_over, delay
    if game_over:
        pen.clear()
        pen.write("Game Over!", align="center", font=("Courier", 36, "bold"))
        time.sleep(2)  # Wait for 2 seconds before restarting
        game_over = False
        snake.reset()
        score = 0
        delay = current_delay
        update_score_display()
        return

    if not paused:
        screen.update()
        check_collisions()
        check_food_collision()
        snake.move_body()
        snake.move()

    screen.ontimer(game_loop, int(delay * 1000))  # Schedule the next iteration


# Keyboard bindings
screen.listen()
screen.onkeypress(snake.go_up, "w")
screen.onkeypress(snake.go_down, "s")
screen.onkeypress(snake.go_left, "a")
screen.onkeypress(snake.go_right, "d")
screen.onkeypress(toggle_pause, "p")
screen.onkeypress(lambda: set_difficulty("easy"), "1")
screen.onkeypress(lambda: set_difficulty("medium"), "2")
screen.onkeypress(lambda: set_difficulty("hard"), "3")

# Set initial delay and start game loop
current_delay = DELAY_MEDIUM

# Start the game loop
game_loop()
screen.mainloop()