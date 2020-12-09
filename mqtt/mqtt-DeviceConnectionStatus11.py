# encoding: utf-8


import paho.mqtt.client as mqtt
import json
import time
import threading


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("MCloud_product_001/+/DeviceConnectionStatus")

def sendBakMessage(client, msg):
    #print(msg.topic + " " + ":" + str(msg.payload))
    topic = msg.topic
    y = '/MCloud_product_001/DeviceConnectionStatusAck'
    m = '/MCloud_product_001/ReportRtData'
    x = topic.split("/")[1]
    t = str(round(time.time() * 1000))
    #year = str(time.strftime("%Y"))
    #month = str(time.strftime("%m"))ERROR   2019-03-25 11:20:15.123 [kg.apc.p] (): Failed to get JMX Connector
    #day = str(time.strftime("%d"))
    #hour = str(time.strftime("%H"))
    #minute = str(time.strftime("%M"))
    #second = str(time.strftime("%S"))
    message = msg.payload
    sen = x + y
    senr = x + m
    mid = json.loads(message)['mid']
    pld = json.loads(message)['pld']['deviceIds'][0]['deviceId']
    client.publish(sen, "{'mid':'" + mid + "','version':'1.0.0','pld':{'deviceIds':[{'deviceId':'"+pld+"','result':1}]}}",2)
    #client.publish(senr, "{'mid':'" + mid + "','version':'1.0.0','pld':{'deviceId':'"+pld+"','array':[{'ts':'"+t+"','datas':['36924,"+year+"','36923,"+month+"','36922,"+day+"','36921,"+hour+"','36920,"+minute+"','36919,"+second+"','36887,1']}]}}",2)
    print (sen + " >> 成功")


def on_message(client, userdata, msg):
    print('start...')
    n = 2
    m = 4
    try:
        t = threading.Thread(target=sendBakMessage, arg=(client,msg))
        t.start()
        t.join()
    except BaseException as e:
        print(e.message)
    print('gone')


def do(n):
    print (n)
    print ('-----------')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("172.16.6.37", 1883, 60)
client.loop_forever()
