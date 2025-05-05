light_value = 0
temperature = 0.0
motor_distance = 999
alarm_distance = 999

light_on = False
heat_on = False
fan_on = False
alarm_enabled = True
alarm_triggered = False
manual = False

def get_state():
    return {
        "light_value": light_value,
        "temperature": temperature,
        "motor_distance": motor_distance,
        "alarm_distance": alarm_distance,
        "light_on": light_on,
        "heat_on": heat_on,
        "fan_on": fan_on,
        "alarm_enabled": alarm_enabled,
        "alarm_triggered": alarm_triggered,
        "manual": manual
    }