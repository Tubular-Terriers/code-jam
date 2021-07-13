import asyncio
import pygame
from pynput import keyboard


def async_wrapper(callback):
    def inner(key):
        asyncio.run(callback(key))
    return inner


@async_wrapper
async def on_press(key):
    await asyncio.sleep(1)
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

pygame.init()

clock = pygame.time.Clock()

crashed = False

counter = 1
while not crashed:
    print(counter)
    counter += 1
    clock.tick(1)  # will be 10 in the next run
