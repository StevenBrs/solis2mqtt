import requests
import re
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time

solisip = "192.168.0.219";
mqttip = "192.168.0.21";

entities = {
        'webdata_now_p':{'name':'Solis Current Power (W)', 'device_class':'power', 'state_class':'measurement', 'unit_of_measurement':'W', 'icon':'mdi:solar-power'}, 
        'webdata_today_e':{'name':'Solis Yield Today (kWh)', 'device_class':'energy', 'state_class':'total_increasing', 'unit_of_measurement':'kWh', 'icon':'mdi:solar-power'}, 
        'webdata_total_e':{'name':'Solis Total Yield (kWh)', 'device_class':'energy', 'state_class':'total_increasing', 'unit_of_measurement':'kWh', 'icon':'mdi:solar-power'}, 
        'webdata_alarm':{'name':'Solis Alarms', 'icon':'mdi:solar-power'}, 
}

def sendEntities():
  mc = mqtt.Client(client_id="solis2mqtt", clean_session=False)
  mc.connect(mqttip)

  for entity in entities:
    entity_id = 'solis_' + entity
    payload = {
      'unique_id':entity_id,
      'valuetemplate':'{{value_json.value}}',
      'state_topic':'homeassistant/sensor/' + entity_id + '/state'
    }
    payload |= entities[entity]
    print('homeassistant/sensor/' + entity_id + '/config', json.dumps(payload))
    mc.publish('homeassistant/sensor/' + entity_id + '/config', payload=json.dumps(payload), retain=True)

  mc.disconnect


def parseSendSolis():
  try:
    page = requests.get('http://' + solisip + '/status.html', auth=('admin', 'admin'))
    html = page.content.decode('utf-8')
  except:
    html = '';

  rawdata = re.findall(r'var webdata_.*;', html)
  data = {}
  for rawvalue in rawdata:
    rawvalueparts = re.search(r'var (.*) = "(.*)";', rawvalue)
    entity = rawvalueparts.group(1)
    value = rawvalueparts.group(2)
    if entity in entities:
      data[entity] = value

  if (data):
    print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' : ' + json.dumps(data))

    mc = mqtt.Client(client_id="solis2mqtt", clean_session=False)
    mc.connect(mqttip)

    for entity in data:
      entity_id = 'solis_' + entity
      payload = {
        'unique_id':entity_id,
        'valuetemplate':'{{value_json.value}}',
        'state_topic':'homeassistant/sensor/' + entity_id + '/state'
      }
      for item in entities[entity]:
        payload[item] = entities[entity][item]

      if (data[entity] != "" or entity == 'webdata_alarm'):
        value = data[entity]
        if (entity == 'webdata_now_p'): value = int(value)
        if (entity == 'webdata_today_e'): value = round(float(value),1)
        if (entity == 'webdata_total_e'): value = round(float(value))
        #print('homeassistant/sensor/' + entity_id + '/state', value)
        mc.publish('homeassistant/sensor/' + entity_id + '/state', payload=value, retain=False)

    mc.disconnect


sendEntities()

while True:
  parseSendSolis()
  time.sleep(60)
