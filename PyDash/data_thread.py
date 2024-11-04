import threading
import sys
import time



class DataThread(threading.Thread): 

    def __init__(self): 
        super(DataThread, self).__init__()
        self.is_running = False
        self.reading = 0 
    
    def run(self): 
        self.is_running = True
        self._loop()

    def stop(self):
        self.is_running = False
    
    def get_reading(self):
        return self.reading

    def _loop(self): 
        count_down = False
        while self.is_running: 
            time.sleep(0.5)
            if self.reading == 100: 
                count_down = True
            if self.reading == 0:
                count_down = False

            if not count_down: 
                self.reading += 1
            
            if count_down: 
                self.reading -= 1
            
             