# solis2mqtt

for use with Solis WiFi dongle and Home Assistant+MQTT 
More info to come...

Usage: 
* Edit solis2mqtt.py and set IP of the Solis WiFi Dongle and the MQTT server 
* Adjust the username and password for the WiFi dongle (not the SolisCloud account)
* Run ./docker.run to spin up a docker container that will run the script

Script will poll the WiFi dongle every 60 seconds, and publish the values to MQTT
It also publishes config info so HA creates the entities automatically
