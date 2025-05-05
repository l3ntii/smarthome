# SmartHome System – Gruppe 14

## Projektbeschreibung
Dieses Projekt entstand im Rahmen der Lehrveranstaltung und verfolgt das Ziel, ein einfaches, aber funktionales Smart-Home-System mit zwei Raspberry Pis zu entwickeln. Dabei werden Sensorwerte erfasst und über MQTT an einen zweiten Pi gesendet, der verschiedene Aktoren steuert. Die Steuerung erfolgt zusätzlich über eine zentrale Benutzeroberfläche.

## Funktionen
- Automatische Lichtsteuerung bei Dunkelheit
- Temperaturmessung mit Visualisierung durch eine LED bzw eines Servomotors
- Steuerung eines Lüfters über einen Servomotor, inkl. Sicherheitsabschaltung bei Annäherung
- Bewegungsmelder mit Alarmfunktion
- Steuerung aller Aktoren über eine einfache grafische Oberfläche
- Kommunikation zwischen den Komponenten über MQTT

## Aufbau des Systems
Das System besteht aus zwei Raspberry Pis:

- **Sensor-Raspberry Pi (RPi 3)**  
  Dieser Pi liest verschiedene Sensoren aus (Temperatur, Licht, Bewegung, Abstand) und sendet die Daten über MQTT.

- **Aktor-Raspberry Pi (RPi 4)**  
  Dieser Pi empfängt die Sensordaten und steuert entsprechend die Aktoren (LEDs, Servo, Buzzer). Außerdem kann über die GUI manuell eingegriffen werden.

Die Kommunikation zwischen beiden Geräten erfolgt über einen MQTT-Broker im lokalen Netzwerk.

## Verwendete Technologien und Komponenten
- Python 3
- MQTT (paho-mqtt)
- Raspberry Pi GPIO
- Sense HAT (Temperatur)
- VL6180X (ToF-Abstandssensor)
- HC-SR04 (Ultraschallsensor)
- Photoresistor (zur Helligkeitserkennung)
- Servo-PWM-HAT (für Lüftersteuerung)
- Verschiedene LEDs und ein Buzzer

## Installation und Inbetriebnahme

### Voraussetzungen
- Zwei Raspberry Pis im selben Netzwerk
- MQTT-Broker (z. B. Mosquitto) installiert und laufend
- Python 3 + benötigte Bibliotheken (siehe unten)
- Verkabelung und Aufbau laut `materialliste.md`

### Vorbereitung
Beide Pis sollten Zugriff auf das Projektverzeichnis erhalten. Das Repository muss geklont und die Abhängigkeiten installiert werden. Außerdem müssen die MQTT-Clients richtig eingestellt werden, da die RPis in  anderen Netzwerken andere IP-Adressen zugeordnet werden.

### Start der Systeme
Auf dem Sensor-RPi:
```bash
cd sensor-rpi
python3 main.py
```

Auf dem Aktor-RPi:
```bash
cd aktor-rpi
python3 smarthome.py
```

Danach kann man über den lokalen Browser auf die Webgui zugreifen unter 'xxx.xxx.xxx.xxx:5000', je nachdem was die IP-Adresse des Aktor-RPis im lokalen Netzwerk ist.

## Demo-Video
Eine Demo-Video findet ihr unter folgenden Link: 
'https://drive.google.com/file/d/1_4T4uNUWU9gPz4-EKh7E4mCaBF9K2JlI/view'


