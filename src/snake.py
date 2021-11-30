import turtle
import random


class Config:
    WIDTH = 500  # Pixels
    HEIGHT = 500  # Pixels
    DELAY = 150  # Miliseconds
    FOOD_SIZE = 10
    BACKGROUND_COLOR = "black"
    SNAKE_SHAPE = "square"
    SNAKE_COLOR = "white"
    FOOD_SHAPE = "circle"
    FOOD_COLOR = "white"
    OFFSETS = {
        "up": (0, 20),
        "down": (0, -20),
        "left": (-20, 0),
        "right": (20, 0),
    }


class Game:

    def __init__(self):
        self.snake_direction = "up"

    def bind_direction_keys(self, screen):
        screen.onkey(lambda: self.set_snake_direction("up"), "Up")
        screen.onkey(lambda: self.set_snake_direction("down"), "Down")
        screen.onkey(lambda: self.set_snake_direction("left"), "Left")
        screen.onkey(lambda: self.set_snake_direction("right"), "Right")

    def set_snake_direction(self, direction):

        if direction == "up":
            if self.snake_direction != "down":
                self.snake_direction = "up"

        if direction == "down":
            if self.snake_direction != "up":
                self.snake_direction = "down"

        if direction == "left":
            if self.snake_direction != "right":
                self.snake_direction = "left"

        if direction == "right":
            if self.snake_direction != "left":
                self.snake_direction = "right"

    def go_up(self):
        if self.snake_direction != "down":
            self.snake_direction = "up"

    def go_down(self):
        if self.snake_direction != "up":
            self.snake_direction = "down"

    def go_left(self):
        if self.snake_direction != "right":
            self.snake_direction = "left"

    def go_right(self):
        if self.snake_direction != "left":
            self.snake_direction = "right"


class Food:
    score = 0

    def __init__(self, position):
        self.position = position

    def food_collision(self, snake, food_turtle):
        if get_distance(snake[-1], self.position) < 20:
            self.score += 1
            self.position = get_random_food_pos()
            food_turtle.goto(self.position)
            return True
        return False


def get_random_food_pos():
    x = random.randint(- int(Config.WIDTH / 2) + Config.FOOD_SIZE, int(Config.WIDTH / 2) - Config.FOOD_SIZE)
    y = random.randint(- int(Config.HEIGHT / 2) + Config.FOOD_SIZE, int(Config.HEIGHT / 2) - Config.FOOD_SIZE)
    return x, y


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    distance = (((y2 - y1) ** 2) + ((x2 - x1) ** 2)) ** 0.5  # Pythogorean theorem

    return distance


def game_loop(game: Game, snake: list, food: Food, snake_turtle, food_turtle, screen):
    snake_turtle.clearstamps()

    new_head = snake[-1].copy()
    new_head[0] += Config.OFFSETS[game.snake_direction][0]
    new_head[1] += Config.OFFSETS[game.snake_direction][1]

    if new_head in snake \
            or new_head[0] < - Config.WIDTH / 2 or new_head[0] > Config.WIDTH / 2 \
            or new_head[1] < - Config.HEIGHT / 2 or new_head[1] > Config.HEIGHT / 2:
        reset(game, snake_turtle, food_turtle, screen)
    else:
        snake.append(new_head)
        if not food.food_collision(snake, food_turtle):
            snake.pop(0)

        for segment in snake:
            snake_turtle.goto(segment[0], segment[1])
            snake_turtle.stamp()

        screen.title(f"Snake \U0001F40D. Score: {food.score}")
        screen.update()

        turtle.ontimer(lambda: game_loop(game, snake, food, snake_turtle, food_turtle, screen), Config.DELAY)


def reset(game: Game, snake_turtle, food_turtle, screen):
    food = Food(get_random_food_pos())
    snake = [[0, 0], [20, 0], [40, 0], [60, 0]]
    food_turtle.goto(food.position)
    game_loop(game, snake, food, snake_turtle, food_turtle, screen)


def run():
    screen = turtle.Screen()
    screen.setup(Config.WIDTH, Config.HEIGHT)
    screen.bgcolor(Config.BACKGROUND_COLOR)
    screen.tracer(0)  # turn off automatic animation
    screen.listen()

    game = Game()
    game.bind_direction_keys(screen)

    snake_turtle = turtle.Turtle()
    snake_turtle.shape(Config.SNAKE_SHAPE)
    snake_turtle.color(Config.SNAKE_COLOR)
    snake_turtle.penup()

    food_turtle = turtle.Turtle()
    food_turtle.shape(Config.FOOD_SHAPE)
    food_turtle.color(Config.FOOD_COLOR)
    food_turtle.shapesize(Config.FOOD_SIZE / 20)
    food_turtle.penup()

    reset(game, snake_turtle, food_turtle, screen)

    turtle.done()
