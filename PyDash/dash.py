import pygame
import asyncio
import signal
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

def sync_call(awaitable, loop): 
    return loop.run_until_complete(awaitable)


async def try_bluetooth(loop, async_shutdown_listeners):  
    bt_task, on_quit = esp32.start_sensors(loop, STATE)
    if bt_task is None: # we've got a problem 
        return False
    loop.create_task(bt_task())
    async_shutdown_listeners.append(lambda: loop.create_task(on_quit()))
    return True


async def start_bluetooth(loop, async_shutdown_listeners): 
    result = await try_bluetooth(loop, async_shutdown_listeners)
    if not result: 
        print('start')

def initialize(loop, shutdown_listeners):
    loop.create_task(start_bluetooth(loop, async_shutdown_listeners=shutdown_listeners))
    def shutdown(sig, frame): 
        global running
        running = False 
        for l in shutdown_listeners:
            loop.run_until_complete(l())
        for t in asyncio.all_tasks(loop):
            t.cancel()
        loop.close()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGHUP, shutdown)
    return shutdown

def temperature_listener(key, value): 
    print("{}: {}".format(key, value))

STATE.register_listener('temperatures.inside', temperature_listener)
STATE.register_listener('temperatures.outside', temperature_listener)

def run(): 
    data_thread = DataThread()
    global running
    # from gauges import text
   

    # pygame setup
    pygame.init()
    screen = None
    if config.FULLSCREEN: 
        screen = pygame.display.set_mode(config.MODE, pygame.FULLSCREEN)
    else: 
        screen = pygame.display.set_mode(config.MODE)
    
    clock = pygame.time.Clock()
    dt = 0

    taco_dash = Dashboard(screen)
    shutdown_listeners = []
    event_loop = asyncio.get_event_loop()
    shutdown = initialize(event_loop, shutdown_listeners)

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
                shutdown(None, None)

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
 

    data_thread.stop()
    data_thread.join()
    pygame.quit()


if __name__ == '__main__': 
    run()