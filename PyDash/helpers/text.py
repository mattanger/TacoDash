import pygame

def render_text(text, color, font=None):
    render_font = pygame.font.SysFont("Arial", 24) if font is None else font
    return render_font.render(text, True, color)