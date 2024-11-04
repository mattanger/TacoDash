import pygame
from .gauge import Gauge
from inputs import counter
from helpers import text
from state import STATE

class TextGauge(Gauge): 
    def __init__(self, position = None) -> None:
        self.position = position

    def fix_coordiantes(self, txt_surface, position):
        x = position[0]
        y = position[1]
        if x < 0:
            x = (self.screen.get_width() - txt_surface.get_width()) + x
        if y < 0:
            y = (self.screen.get_height() - txt_surface.get_height() ) + y
        return (x,y)
    
    def set_screen(self, screen):
        self.screen = screen

    def set_position(self, position):
        self.position = position
    
    def get_position(self):
        return self.position
    
    def get_data(self):
        raise NotImplementedError("This method requires implementation")

    def render(self): 
        surface = text.render_text(self.get_data(), "WHITE")
        self.screen.blit(surface, self.fix_coordiantes(surface, self.position))


class Clock(TextGauge): 
    """
    """
    def __init__(self, position=None) -> None:
        super().__init__(position)

    def get_data(self):
        return counter.get_time()


class Temperature(TextGauge):
    """

    """
    SENSOR_NAMES = {
        "outside": "Outside",
        "inside": "Inside",
        "intake_1": "Intake_1",
        "intake_2": "Intake_2"
    }
    def __init__(self, sensor, position=None) -> None:
        super().__init__(position)
        self.sensor = sensor
        self.temperature = 0
        STATE.register_listener(attr="temperatures.{}".format(self.sensor), listener=self)

    def notify(self, attr, value): 
        self.temperature = value

    def get_data(self): 
        return "{}: {}".format(self.SENSOR_NAMES[self.sensor], self.temperature)
