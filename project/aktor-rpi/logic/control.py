import time
import config
from state import state
from logic import actions

def run():
    try:
        while True:
            if not state.manual:
                if state.light_value > config.LIGHT_THRESHOLD:
                    state.light_on = True
                    actions.set_light(True)
                else:
                    state.light_on = False
                    actions.set_light(False)

                if state.temperature < config.TEMP_THRESHOLD_HEAT:
                    state.heat_on = True
                    state.fan_on = False
                    actions.set_heat(True)
                    actions.set_fan(False)
                elif state.temperature > config.TEMP_THRESHOLD_FAN:
                    state.heat_on = False
                    state.fan_on = True
                    actions.set_heat(False)
                    actions.set_fan(True)
                else:
                    state.heat_on = False
                    state.fan_on = False
                    actions.set_heat(False)
                    actions.set_fan(False)

            if state.fan_on and state.motor_distance < config.SAFETY_DISTANCE_MM:
                actions.set_fan(False)
                state.fan_on = False

            if state.alarm_enabled and state.alarm_distance < config.ALARM_DISTANCE_CM:
                if not state.alarm_triggered:
                state.alarm_triggered = True
            else:
                if state.alarm_triggered:
                state.alarm_triggered = False

            if state.alarm_triggered:
                actions.buzzer_on()
                time.sleep(0.2)
                actions.buzzer_off()
                time.sleep(0.8)
            else:
                time.sleep(0.5)

    except KeyboardInterrupt:
        actions.cleanup()