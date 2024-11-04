from helpers import text
from inputs import counter
# from gauges.text import * 

from state import STATE
import config

class Dashboard: 
    def __init__(self, screen) -> None:
        self.screen = screen
        self.gauges = [] 
        self.inputs = {}
        self.init_from_config()
    
    def init_from_config(self): 
        module = __import__("gauges")
        for g in config.DASHBOARD["gauges"]:
            class_ = getattr(module, g) 
            instance = class_(**config.DASHBOARD["gauges"][g])
            instance.set_screen(self.screen)
            self.gauges.append(instance)
        
    def register_gauge(self, gauge): 
        pass
    
    def register_inputs(self, input):
        pass

    def render_dashboard(self):
        for gauge in self.gauges:  
            gauge.render()