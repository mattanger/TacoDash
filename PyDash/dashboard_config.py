BACKGROUND_COLOR = (30, 19, 34)

DASHBOARD = {
    "gauges": [
        {
            "gauge": "Clock",
            "params": {
                "position": (-10, 10),
                "color": (137, 148, 153),
                "time_format": "%H:%M",
                "font_size": 48
            }
        },
        {
            "gauge": "Temperature",
            "params": {
                "sensor": "outside",
                "position": (1150,60),
                "font_size": 36,
                "title_font_size": 22
            }
        },
        {
            "gauge": "Temperature",
            "params": {
                "sensor": "inside",
                "position": (1240,60),
                "font_size": 36,
                "title_font_size": 22
            }
        }
    ]
        
}