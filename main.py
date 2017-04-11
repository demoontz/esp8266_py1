WIFISSID='=<^-^>='
WIFIPASS='44448888'

from machine import Pin
from machine import I2C
from machine import unique_id
from time import sleep_ms
from ubinascii import hexlify
from umqtt.simple import MQTTClient
import network
# from machine import ADC
from dht import DHT11
from ssd1306 import SSD1306_I2C


#init hardware

#---OLED 128x64---
i2c = I2C(sda = Pin(4), scl = Pin(5))
oled = SSD1306_I2C(128, 64, i2c)
#---DHT22---
ds = DHT11(Pin(16)) #DHT22 connected to GPIO16
#---led---
led = Pin(2, Pin.OUT)
rl1 = Pin(14, Pin.OUT)
rl2 = Pin(12, Pin.OUT)

#---MQTT Sending---
SERVER = "10.10.1.120"
CLIENT_ID = hexlify(unique_id())
tempr = b"/sensor1/tem"
humd = b"/sensor1/hum"
rel1top = b"/sensor1/sw1"
rel2top = b"/sensor1/sw2"

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        led.low()
        oled.fill(0)
        oled.text('wifi...', 0, 0)
        oled.show()
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFISSID, WIFIPASS)
        while not sta_if.isconnected():
            pass
        oled.text('done...', 0, 10)
        led.high()
        print('network config:', sta_if.ifconfig())

def envioMQTT(server=SERVER, topic="/foo", dato=None):
    try:
        c = MQTTClient(CLIENT_ID, server)
        c.connect()
        c.publish(topic, dato)
        sleep_ms(200)
        c.disconnect()
    except Exception as e:
        print ("mqq fail")
        pass


def sub_cb(topic, msg):
    if topic==rel1top:
        if msg == b"on":
            rl1.low()
            print("sw1 on")
        elif msg == b"off":
            rl1.high()
            print("sw1 off")

    if topic==rel2top:
        if msg == b"on":
            rl2.low()
            print("sw2 on")
        elif msg == b"off":
            rl2.high()
            print("sw2 off")



def recepcionMQTT(server=SERVER, topic=rel2top):
    c = MQTTClient(CLIENT_ID, server)
    # Subscribed messages will be delivered to this callback
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(topic)
    #print("Connected to %s, subscribed to %s topic" % (server, topic))
    try:
        c.wait_msg()
    finally:
        c.disconnect()

def medirTemHum():
    try:
        ds.measure()
        tem = ds.temperature()
        hum = ds.humidity()
        return (tem,hum)
    except Exception as e:
        return (-1,-1)

def displaytem(tem,hum):
    oled.fill(0)
    temper = "Tem: %3.1f C" % tem
    humedad = "Hum: %3.1f %%RH" % hum

    oled.text(temper,2,2,1)
    oled.text(humedad,2,14,1)
    oled.text("SW1 "+str(rl1.value()), 2, 40, 1)
    oled.text("SW2 "+str(rl2.value()), 50, 40, 1)
    oled.show()

def measureDist():
    pass

#---Main Program---
print("main run")
while True:
    print("loop run")
    try:
        do_connect()
        measureDist()
        (tem,hum) = medirTemHum()
        displaytem(tem,hum)
        envioMQTT(SERVER,tempr,str(tem))
        envioMQTT(SERVER,humd,str(hum))
        recepcionMQTT(SERVER, rel1top)
        recepcionMQTT(SERVER, rel2top)
        sleep_ms(1000)
    except Exception as e:
        print (e)
        print ("fuck up =)")
        pass
#---END Main Program---
