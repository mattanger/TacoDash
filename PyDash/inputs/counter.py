from datetime import datetime

def get_time():
    return datetime.now().strftime('%m/%d/%y %H:%M:%S')