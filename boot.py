def do_connect():
    print("board start")
    import network
    import ssd1306
    import network
    import time
    from machine import Pin, I2C
    i2c = I2C(scl=Pin(5), sda=Pin(4))
    i2c.scan()
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.text('Hi, dude!', 30, 30)
    oled.show()
    SSID = 'Ciklum Guest'
    PASSWORD = 'Welcome2Ciklum'

    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)
    if ap_if.active():
        ap_if.active(False)
    if not sta_if.isconnected():
        oled.text('conn2wifi...', 0, 0)
        oled.show()
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    oled.text('wifi:', 0, 10)
    oled.text(str(sta_if.ifconfig()), 0, 20)
    oled.show()
do_connect()
