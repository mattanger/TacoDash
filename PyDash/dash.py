import pygame
import asyncio
import signal
import functools
import sys
from data_thread import DataThread

from random import randint

from pygame.locals import *
from state import STATE
import config
import esp32
import gauges.dial

from dashboard import Dashboard
running = True
def run_event_loop(loop): 
    loop.call_soon(loop.stop)
    loop.run_forever()

async def end_call():
    await asyncio.sleep(0.5)

async def start_bluetooth(loop, shudown_listeners):  
    bt_task, on_quit = await esp32.start_sensors(loop, STATE) 
    loop.create_task(bt_task())
    shudown_listeners.append(lambda: loop.create_task(on_quit()))

def shutdown(sig, frame): 
    global running
    running = False 
    # loop.stop()
    # pygame.quit()
    # sys.exit(0)

def initialize(loop, shutdown_listeners):
    loop.create_task(start_bluetooth(loop, shudown_listeners=shutdown_listeners))
    # sf = functools.partial(shutdown, loop, shutdown_listeners)
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGHUP, shutdown)
    # loop.add_signal_handler(signal.SIGHUP, sf)
    # loop.add_signal_handler(signal.SIGTERM, sf)
    # loop.add_signal_handler(signal.SIGINT, sf)

def temperature_listener(key, value): 
    print("{}: {}".format(key, value))

STATE.register_listener('temperatures.inside', temperature_listener)
STATE.register_listener('temperatures.outside', temperature_listener)

def run(): 
    data_thread = DataThread()
    global running
    # from gauges import text
    HEIGHT = 1280
    WIDTH = 720
    MODE = (HEIGHT, WIDTH)

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode(MODE)
    clock = pygame.time.Clock()
    dt = 0

    taco_dash = Dashboard(screen)
    shutdown_listeners = []
    event_loop = asyncio.get_event_loop()
    initialize(event_loop, shutdown_listeners)

    per_gauge = gauges.dial.ArcBarGauge(
              screen=screen,
                position=(10,10),
                thickness=50,
                radius=200,
                range=(0,100),
                fill_color=(126, 245, 95))

    speed_gauge = gauges.dial.DialGauge(
        screen, 
        (10, 420),
        200,
        range=(0, 110),
        fill_color=(100, 20, 150)
    )

    tack = gauges.dial.DialGauge(
        screen, 
        (420, 10),
        200,
        range=(0, 110),
        fill_color=(100, 20, 150)
    )

    data_thread.start()
    while running:
        run_event_loop(event_loop)
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill((30, 19, 34))

        taco_dash.render_dashboard()

        # percentage = randint(77, 84)
        per_gauge.draw(percent=data_thread.get_reading())
        speed_gauge.draw()
        tack.draw()


        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(6) / 1000

    for l in shutdown_listeners:
        l()

    for t in asyncio.all_tasks(event_loop):
        t.cancel()
    
    data_thread.stop()
    data_thread.join()
    event_loop.close()
    pygame.quit()


if __name__ == '__main__': 
    run()