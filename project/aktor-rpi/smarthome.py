import threading
import time
from datetime import datetime
from flask import Flask, render_template_string, jsonify
from logic import actions, control
from mqtt import subscriber
from state import state

app = Flask(__name__)

measurements = []

HTML_PAGE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartHome Steuerung</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f2f2;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #007acc;
        }
        .section {
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .btn {
            padding: 15px 25px;
            font-size: 16px;
            margin: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .btn-on { background: #4CAF50; color: white; }
        .btn-off { background: #f44336; color: white; }
        .btn-disabled { background: #aaa; color: #eee; cursor: not-allowed; }
        .device-buttons {
            display: none;
        }
        .visible {
            display: block;
        }
    </style>
</head>
<body>
    <h1>SmartHome Steuerung</h1>

    <div class="section">
        <h2>Systemstatus</h2>
        <p>Modus: <span id="mode">...</span></p>
        <p>Alarm: <span id="alarm">...</span></p>
    </div>

    <div class="section">
        <button class="btn" onclick="toggleAlarm()" id="alarmBtn">Alarm EIN/AUS</button>
        <button class="btn" onclick="toggleManual()" id="manualBtn">Manuelle Steuerung EIN/AUS</button>
    </div>

    <div class="section device-buttons" id="manualControls">
        <h2>Manuelle Steuerung</h2>
        <button class="btn" onclick="toggleLight()" id="lightBtn">Licht AN/AUS</button>
        <button class="btn" onclick="toggleHeat()" id="heatBtn">Heizung AN/AUS</button>
        <button class="btn" onclick="toggleFan()" id="fanBtn">Ventilator AN/AUS</button>
    </div>

    <div class="section">
        <h2>Letzte 5 Messungen</h2>
        <ul id="measurementList"></ul>
    </div>

    <div class="section">
        <h2>Alarm-Ereignisse</h2>
        <ul id="alarmLog"></ul>
    </div>

    <script>
        let state = {};
        let lastAlarmState = false;

        async function fetchState() {
            const response = await fetch('/state');
            state = await response.json();
            updateUI();
        }

        async function fetchMeasurements() {
            const res = await fetch('/measurements');
            const list = await res.json();
            const ul = document.getElementById("measurementList");
            ul.innerHTML = "";
            list.forEach(item => {
                const li = document.createElement("li");
                li.textContent = item;
                ul.appendChild(li);
            });
        }

        function updateUI() {
            document.getElementById('mode').textContent = state.manual ? 'Manuell' : 'Automatik';
            document.getElementById('alarm').textContent = state.alarm_enabled ? 'Scharf' : 'Aus';

            document.getElementById('manualControls').classList.toggle('visible', state.manual);

            const alarmBtn = document.getElementById('alarmBtn');
            alarmBtn.className = 'btn ' + (state.alarm_enabled ? 'btn-on' : 'btn-off');

            const manualBtn = document.getElementById('manualBtn');
            manualBtn.className = 'btn ' + (state.manual ? 'btn-on' : 'btn-off');

            const devices = ['light', 'heat', 'fan'];
            devices.forEach(dev => {
                const btn = document.getElementById(dev + 'Btn');
                const isOn = state[dev + '_on'];
                btn.className = 'btn ' + (isOn ? 'btn-on' : 'btn-off');
                if (!state.manual) btn.classList.add('btn-disabled');
                else btn.classList.remove('btn-disabled');
            });

            if (state.alarm_triggered && !lastAlarmState) {
                const ul = document.getElementById("alarmLog");
                const li = document.createElement("li");
                const now = new Date().toLocaleTimeString();
                li.textContent = `[${now}] Alarm ausgelöst`;
                ul.prepend(li);
                while (ul.children.length > 5) {
                    ul.removeChild(ul.lastChild);
                }
            }
            lastAlarmState = state.alarm_triggered;
        }

        async function post(endpoint) {
            await fetch(endpoint, { method: 'POST' });
            fetchState();
            fetchMeasurements();
        }

        const toggleAlarm = () => post('/toggle_alarm');
        const toggleManual = () => post('/toggle_manual');
        const toggleLight = () => state.manual && post('/toggle_light');
        const toggleHeat = () => state.manual && post('/toggle_heat');
        const toggleFan = () => state.manual && post('/toggle_fan');

        fetchState();
        fetchMeasurements();
        setInterval(() => {
            fetchState();
            fetchMeasurements();
        }, 5000);
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/state")
def get_state():
    return jsonify(state.get_state())

@app.route("/measurements")
def get_measurements():
    return jsonify(measurements)

@app.route("/toggle_alarm", methods=["POST"])
def toggle_alarm():
    state.alarm_enabled = not state.alarm_enabled
    return '', 204

@app.route("/toggle_manual", methods=["POST"])
def toggle_manual():
    state.manual = not state.manual
    if state.manual:
        state.light_on = False
        state.fan_on = False
        state.heat_on = False
        actions.set_light(False)
        actions.set_fan(False)
        actions.set_heat(False)
    return '', 204

@app.route("/toggle_light", methods=["POST"])
def toggle_light():
    state.light_on = not state.light_on
    actions.set_light(state.light_on)
    return '', 204

@app.route("/toggle_heat", methods=["POST"])
def toggle_heat():
    state.heat_on = not state.heat_on
    actions.set_heat(state.heat_on)
    return '', 204

@app.route("/toggle_fan", methods=["POST"])
def toggle_fan():
    state.fan_on = not state.fan_on
    actions.set_fan(state.fan_on)
    return '', 204

def update_measurements():
    time.sleep(5)
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        entry = f"[{now}] Temp: {state.temperature:.1f}°C, Licht: {state.light_value}, Abstand Motor: {state.motor_distance} mm, Abstand Alarm: {state.alarm_distance} cm"
        measurements.insert(0, entry)
        if len(measurements) > 5:
            measurements.pop()
        time.sleep(5)

def main():
    print("SmartHome System startet...")
    try:
        threading.Thread(target=subscriber.start, daemon=True).start()
        threading.Thread(target=control.run, daemon=True).start()
        threading.Thread(target=update_measurements, daemon=True).start()
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        print("\n[INFO] SmartHome wird beendet – Aktoren ausschalten...")
    finally:
        actions.set_light(False)
        actions.set_heat(False)
        actions.set_fan(False)
        actions.set_buzzer(False)
        actions.cleanup()
        print("[INFO] GPIOs freigegeben. Shutdown abgeschlossen.")

if __name__ == "__main__":
    main()