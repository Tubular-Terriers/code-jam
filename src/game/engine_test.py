""" pygame.init()

clock = pygame.time.Clock()

crashed = False

counter = 1
while not crashed:
    print(counter)
    counter += 1
    clock.tick(30)  # will be 10 in the next run """

import pygame
import pymunk  # Import pymunk..
import pymunk.pygame_util

pygame.init()
size = 640, 320
screen = pygame.display.set_mode(size)
draw_options = pymunk.pygame_util.DrawOptions(screen)

space = pymunk.Space()  # Create a Space which contain the simulation
space.gravity = 0, 0  # Set its gravity

body = pymunk.Body(1, 1666)  # Create a Body with mass and moment
body.position = 50, 100  # Set the position of the body

poly = pymunk.Poly.create_box(body)  # Create a box shape and attach to body
space.add(body, poly)  # Add both body and shape to the simulation

print_options = pymunk.SpaceDebugDrawOptions()  # For easy printing

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("red")
    space.debug_draw(draw_options)
    pygame.display.update()
    space.step(0.01)

pygame.quit()

step = 10
for i in range(1, step + 1):  # Infinite loop simulation
    space.step(0.001 / i)  # Step the simulation one step forward
    space.debug_draw(print_options)  # Print the state of the simulation
