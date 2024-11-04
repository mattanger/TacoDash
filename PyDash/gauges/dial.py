import pygame
import plotly.graph_objects as go
import io
from PIL import Image

import pygame.gfxdraw
import math
import serial
from random import randint
import config


def generate_dial(r_start, r_end): 
    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = 0,
    mode = "gauge+number+delta",
    title = {'text': "Speed"},
    # delta = {'reference': 380},
    gauge = {'axis': {'range': [None, 110]},
             'steps' : [
                 {'range': [0, 110], 'color': "lightgray"},
                 {'range': [85, 110], 'color': "gray"}],
             'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 0}}))
    fig.update_layout(paper_bgcolor="rgb(30, 19, 34)")
    return fig.to_image(format="png")

def draw(screen, position):
    img_bytes = generate_dial(1,1)
    dial_img = Image.open(io.BytesIO(img_bytes))
    dial = pygame.image.frombuffer(dial_img.tobytes(), dial_img.size, dial_img.mode)
    screen.blit(dial, (10,10))

class RoundGauge: 
    def __init__(self, screen, position: tuple, radius: int, fill_color: tuple, range: tuple):
        self.screen = screen
        self.value_font_size = 75
        self.title_font_size = 36
        self.subtitle_font_size = 28
        self.indicator_font_size = 24
        self.indicator_font_name = config.DEFAULT_FONT_NAME
        self.value_font_name = config.DEFAULT_FONT_NAME
        self.title_font_name = config.DEFAULT_FONT_NAME
        self.subtitle_font_name = config.DEFAULT_FONT_NAME
        
        self.x_cord = position[0] + radius
        self.y_cord = position[1] + radius
        self.range_s = range[0]
        self.range_e = range[1]
        self.thickness = 15
        self.radius = radius
        self.fill_color = fill_color

class ArcBarGauge:

    def __init__(self, screen, position, thickness, radius, circle_colour, **kwargs):
        self.screen = screen
        self.Font = pygame.font.SysFont('ARIAL', 75)


        self.x_cord = position[0] + radius
        self.y_cord = position[1] + radius
        self.thickness = thickness
        self.radius = radius
        self.circle_colour = circle_colour

        self.__dict__.update(kwargs)

    def draw(self, percent):
        fill_angle = int(percent * 270 / 100)
        per = percent
        if percent > 100:
            percent = 100
        if per <= 40:
            per = 0
        if per > 100:
            per = 100

        ac = [255-int(self.circle_colour[0] * per/100),
                255-int(self.circle_colour[1] * per/100),
                255-int(self.circle_colour[2] * per/100)]

        for indexi in range(len(ac)):
            if ac[indexi] < 0:
                ac[indexi] = 0
            if ac[indexi] > 255:
                ac[indexi] = 255


        pertext = self.Font.render(str(percent) + "%", True, ac)
        pertext_rect = pertext.get_rect(center=(int(self.x_cord), int(self.y_cord)))
        self.screen.blit(pertext, pertext_rect)

        for i in range(0, self.thickness):
            pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius - i, -225, 270 - 225, self.circle_colour)
            if percent > 4:
                pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius - i, -225, fill_angle - 225 - 8, ac)

        if percent < 4:
            return



class DialGauge(RoundGauge):

    def __init__(self, screen, position, radius, fill_color, range, **kwargs):
        super().__init__(screen, position, radius, fill_color, range)

        self.start_angle = -237
        self.stop_angle = 57
        self.value = 33 
        self.title = ""
        self.subtitle = ""
        self.value_text_color = (255,255,255)
        self.tick_val_text_color = (255,255,255)
        self.title_text_color = (255,255,255)
        self.tick_color = (20,255,10)
        self.subtick_color = (255,255,255)
        self.dial_color = (255,255,255)
        self.background_color = (47,79,79)
        self.start_angle = 36 
        self.end_angle = 144
        self.major_increments = 10
        self.minor_increments = 10

        self.__dict__.update(kwargs) 

        self.Font = pygame.font.SysFont('ARIAL', self.value_font_size)
        self.title_font = pygame.font.SysFont('ARIAL', self.title_font_size) 
        self.ind_font = pygame.font.SysFont('ARIAL', self.indicator_font_size)

               
    def update_value(self, val): 
        self.value = val

    def dial_indicators():  
        pass

    def draw_center_text(self): 
        value_text = self.Font.render(str(self.value), True, self.value_text_color)
        rect = value_text.get_rect(center=(int(self.x_cord), int(self.y_cord)))
        self.screen.blit(value_text, rect)
        title_text = self.title_font.render(self.title, True, self.title_text_color)
        title_rect = title_text.get_rect(center=(int(self.x_cord), int(self.y_cord + rect.height)))
        self.screen.blit(title_text, title_rect)

    def draw_dial(self): 
        arc = (360 - ( self.end_angle - self.start_angle ) )
        dial_angle = ((arc / self.range_e) * self.value) + 54
        vec = pygame.math.Vector2(0, self.radius - self.thickness).rotate(dial_angle)
        pygame.draw.line(self.screen, self.dial_color, (self.x_cord, self.y_cord), (self.x_cord + vec.x, self.y_cord + vec.y), 2)




    def draw(self):
        pygame.gfxdraw.aacircle(self.screen, self.x_cord, self.y_cord, self.radius + 3, self.background_color)
        pygame.gfxdraw.aacircle(self.screen, self.x_cord, self.y_cord, self.radius, self.fill_color)
        pygame.gfxdraw.filled_circle(self.screen, self.x_cord, self.y_cord, self.radius, self.fill_color)
        pygame.gfxdraw.aacircle(self.screen, self.x_cord, self.y_cord, self.radius - self.thickness, self.fill_color)
        pygame.gfxdraw.filled_circle(self.screen, self.x_cord, self.y_cord, self.radius - self.thickness, self.background_color)


        self.draw_dial()
        self.draw_center_text()
        
        for i in range(0, self.thickness + 5): 
            pygame.gfxdraw.arc(self.screen, int(self.x_cord), int(self.y_cord), self.radius - i, self.start_angle, self.end_angle, config.BACKGROUND_COLOR)

        arc = 360 - ( self.end_angle - self.start_angle )
        step_angle = arc / int(self.range_e / self.major_increments) # the size of each step slice 
        print(step_angle)
        step_range = int(self.range_e / self.major_increments) # the number of slices

        substep_angle = step_angle / self.major_increments
        ticks_start_angle = (self.end_angle - self.start_angle) / 2 # where the gauge starts on the circle 
        tick_angle = ticks_start_angle # where to start first 

        for i in range(0, self.range_e, self.major_increments):
            vec_2 = pygame.math.Vector2(0, self.radius - self.thickness - 5).rotate(tick_angle)
            vec_3 = pygame.math.Vector2(0, self.radius + 10).rotate(tick_angle)
            x_1, y_1 = self.x_cord + vec_2.x, self.y_cord + vec_2.y
            x_2, y_2 = self.x_cord + vec_3.x, self.y_cord + vec_3.y

            # draw major tick on gauge circle 
            pygame.draw.line(self.screen, self.tick_color, (x_1, y_1), (x_2, y_2), 2) 

            # draw tick label on gauge circle 
            txt = self.ind_font.render(str(i), True, self.tick_val_text_color)
            tvec2 = pygame.math.Vector2(0, self.radius - self.thickness - 30).rotate(tick_angle)
            txt_rec = txt.get_rect(center = (self.x_cord + tvec2.x, self.y_cord + tvec2.y))
            self.screen.blit(txt, txt_rec)

            # draw sub steps gradiations 
            subtick_angle = tick_angle + substep_angle
            highlight = int(self.minor_increments / 2) - 1 
            for j in range(0, self.minor_increments): 
                vec_2 = pygame.math.Vector2(0, self.radius - self.thickness).rotate(subtick_angle)
                if j == highlight: 
                    end_len = self.radius + 8
                    color = (255,0,0)
                    width = 4
                else:  
                    end_len = self.radius + 5
                    color = self.subtick_color
                    width = 2
                vec_3 = pygame.math.Vector2(0, end_len).rotate(subtick_angle)
                x_1, y_1 = self.x_cord + vec_2.x, self.y_cord + vec_2.y
                x_2, y_2 = self.x_cord + vec_3.x, self.y_cord + vec_3.y

                pygame.draw.line(self.screen, color, (x_1, y_1), (x_2, y_2), width) 
                
                subtick_angle += substep_angle
            tick_angle += step_angle
 