def dot_traverse(key, value=None): 
    if '.' in key: 
        parts = key.split('.')


class State: 
    """
    This is a holder thing for managing sensor data distributed through the system. 
    It's probably too slow for things like TACH and other really fast stuff, works for temp? 
    """
    def __init__(self) -> None:
        self.state = {
            'temperatures': {}
        }
        self.listeners = {}

    def register_listener(self, attr, listener):
        if attr not in self.listeners: 
            self.listeners[attr] = []
        self.listeners[attr].append(listener)

    def put(self, key, value): 
        self._put(key, value)
        self.notify_listeners(key, value)

    def _put(self, key, value, d = {}): 
        if "." in key:
            key, rest = key.split(".", 1)
            if key not in self.state:
                self.state[key] = {}
            self._put(rest, value, self.state[key])
        else:
            self.state[key] = value 
    
    def get(self, key):
        if "." in key:
            key, rest = key.split(".", 1)
            return self.get_value(self.state[key], rest)
        else:
            return self.state[key]


    def notify_listeners(self, attr, value): 
        if attr not in self.listeners: 
            return

        for l in self.listeners[attr]: 
            if callable(l): 
                l(attr, value)
            elif hasattr(l, 'notify'):
                l.notify(attr, value)
                

    def request(self, attr):
        return ""

    def set_outside_temp(self, temperature): 
        self.put['temperatures.outside'] = temperature
    
    def set_inside_temp(self, temperature): 
        self.put['temperatures.inside'] = temperature


STATE = State()