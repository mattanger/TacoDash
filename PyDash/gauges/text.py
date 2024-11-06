import pygame
from .gauge import Gauge
from inputs import counter
from helpers import text
from state import STATE
import config
from datetime import datetime

# def get_time():

class TextGauge(Gauge): 
    def __init__(self, position = None, **kwargs) -> None:
        self.position = position
        self.color = (255,255,255)
        self.font_size = 24
        self.font_name = config.DEFAULT_FONT_NAME
        self.__dict__.update(kwargs)
        self.font = pygame.font.SysFont(self.font_name, self.font_size)

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
        self.date_format = "%m/%d/%y" 
        self.time_format = "%H:%M:%S"
        self.include_date = False
        super(Clock, self).__init__(position, **kwargs)
        print(self.font_size)

    def get_format(self): 
        format = ""
        if self.include_date: 
            format += self.date_format + " "
        return format + self.time_format 

    def get_data(self):
        return datetime.now().strftime(self.get_format())


class Temperature(TextGauge):
    HOT = 26
    COLD = 4.4
   
    def __init__(self, sensor, title = None, position=None, scale = "C", **kwargs) -> None:
        self.sensor = sensor
        self.temperature = 0
        self.color = (0, 0, 0)
        self.scale = scale
        self.title_font_size = 18
        self.title_font_name = config.DEFAULT_FONT_NAME
        self.title_color = (255,255,255)
        STATE.register_listener(attr="temperatures.{}".format(self.sensor), listener=self)
        super(Temperature, self).__init__(position, **kwargs)
        self.title_font = pygame.font.SysFont(self.title_font_name, self.title_font_size)

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
        title_txt_surface = self.title_font.render(self.sensor.title(), True, color)
        txt_rect = txt_surface.get_rect(center=self.position)
        title_rect = title_txt_surface.get_rect(center=(self.position[0], self.position[1] + txt_rect.height))
        self.screen.blit(txt_surface, txt_rect)
        self.screen.blit(title_txt_surface, title_rect)
