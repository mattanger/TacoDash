import pygame
from .gauge import Gauge
from inputs import counter
from helpers import text
from state import STATE
import config

class TextGauge(Gauge): 
    def __init__(self, position = None, **kwargs) -> None:
        self.position = position
        self.color = (255,255,255)
        self.font_size = 24
        self.__dict__.update(kwargs)
        print(kwargs)
        print(self.font_size)
        self.font = pygame.font.SysFont(config.DEFAULT_FONT_NAME, self.font_size)

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

    def draw(self): 
        surface = text.render_text(self.get_data(), self.color)
        self.screen.blit(surface, self.fix_coordiantes(surface, self.position))


class Clock(TextGauge): 
    """
    """
    def __init__(self, position=None, **kwargs) -> None:
        super(Clock, self).__init__(position, kwargs=kwargs)

    def get_data(self):
        return counter.get_time()


class Temperature(TextGauge):
    HOT = 26
    COLD = 4.4
   
    def __init__(self, sensor, title = "", position=None, scale = "C", **kwargs) -> None:
        self.sensor = sensor
        self.temperature = 0
        self.color = (0, 0, 0)
        self.scale = scale
        STATE.register_listener(attr="temperatures.{}".format(self.sensor), listener=self)
        super(Temperature, self).__init__(position, **kwargs)

    def notify(self, attr, value): 
        self.temperature = float(value) 

    def get_temp_string(self):
        return "{}°{}".format(self.convert_scale(), self.scale)

    def get_data(self): 
        return "{}".format(self.temperature)

    def calculate_color(self): 
        min_temp = -20
        max_temp = 49
        ratio = 2 * (self.temperature - min_temp) / (max_temp - min_temp)
        b = int( max( 0, 255 * (1 - ratio) ) )
        r = int(max(0, 255 * (ratio - 1)))
        g = 255 - b - r
        return r, g, b

    def convert_scale(self): 
        temp = self.temperature
        return int(round(temp)) 
    
    def convert_to_F(self, temp): 
        return temp * 1.8 * 32

    def convert_to_K(self, temp): 
        return temp + 273.15

    def draw(self):  
        color = self.calculate_color()
        txt_surface = self.font.render(self.get_temp_string(), True, color) 
        txt_rect = txt_surface.get_rect(center=self.position)
        self.screen.blit(txt_surface, txt_rect)
