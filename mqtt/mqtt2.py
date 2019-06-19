# encoding: utf-8


import paho.mqtt.client as mqtt
import json
import threadpool


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("MCloud_product_001/+/DeviceConnectionStatus")


def on_message(client, userdata, msg):
    try:
        param = [client, msg]
        data = [(param, None)]
        pool = threadpool.ThreadPool(10)
        requests = threadpool.makeRequests(sendBakMessage, data)
        [pool.putRequest(req) for req in requests]
        # pool.wait()
    except Exception, e:
        print e.message


def sendBakMessage(client, msg):
    try:
        print msg.topic + " " + ":" + str(msg.payload)
        topic = msg.topic.encode("utf-8")
        y = '/MCloud_product_001/DeviceConnectionStatusAck'
        x = topic.split("/")[1]
        message = msg.payload.encode("utf-8")
        sen = x + y
        print sen
        mid = json.loads(message)['mid']
        print 'mid: '+mid
        mes = 'this is ok test'
        # client.publish(sen, "{'mid':'" + mid + "','version':'1.0.0','pld':{'deviceIds':"
        #                                        "[{'deviceId':'MWSS','result':0}]}}")
        client.publish(sen, mes,2)
        print sen + " >> 成功"
    except Exception, e:
        print e.message

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("172.16.6.37", 1883, 60)
client.loop_forever()
