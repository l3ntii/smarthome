## Benutzerhinweise für die Gruppenmitglieder
### Zugangsdaten zum SensorRPi (Raspberry Pi 3): 
user: admin
password: password

### Zugangsdaten zum AktorRPi (Raspberry Pi 4): 
user: admin
password: admin 

SSH sowie I²C sind auf beiden RPis aktiviert. Die RPis über LAN-Kabeln am Router anschließen.
Um sich mit den RPis zu verbinden, müsst ihr euch in euren Router loggen, um die IP-Adressen der RPis herauszufinden. Mit 'ssh admin@192.168.xxx.xxx' könnt ihr dann eine Verbindung aufbauen. 
Die IP-Adresse könnt ihr auch direkt über den RPi rausbekommen, ihr braucht aber eine Maus und Tastatur sowie HDMI- und Micro-HDMI Kabel. Der MQTT-Broker läuft auf dem AktorRPi.

In den Ordnern 'sensor-rpi' bzw. 'aktor-rpi' sind alle Dateien des Projektes. 
