from machine import UART, SoftI2C, Pin
from finger import *
import time
import ssd1306

class FRP():
    def __init__(self):
        self.i2c = SoftI2C(scl = Pin(22), sda=Pin(21))
        self.oled_width = 128
        self.oled_height = 64
        self.oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
        self.fingerSerial = UART(2)
        self.fingerSerial.init(57600, bits=8, parity=None,stop=1) 
        self.f = finger(fingerSerial)

    def EnrollUser(self):
        post = self.f.getTemplateCount() + 1
        p = -1
        print("Place your finger")
        while (p != True):
            p = self.f.readImage()
            if p == True:
                print("Image Taken")
        p = self.f.convertImage(charBufferNumber=FINGERPRINT_CHARBUFFER1)
        if p == True:
            print("Image Coverted")
        
        print('Remove Finger')
        time.sleep(2)
        p = -1
        print("Place Same finger Again")
        while (p != True):
            p = self.f.readImage()
        p = self.f.convertImage(charBufferNumber=FINGERPRINT_CHARBUFFER2)
        if p == False:
            if p == True:
                print("Finger Print Matched")
        print("Creating Template")
        p = self.f.createTemplate()
        p = self.f.storeTemplate(positionNumber=post, charBufferNumber=FINGERPRINT_CHARBUFFER1)
        if p == post:
            print("Register Successfull")
        else:
            print("Something went wrong")

    
    def SearchUser(self):
        p = -1
        while (p != True):
            p = self.f.readImage()
        p = self.f.convertImage()
        res = self.f.searchTemplate(p)
        if res[0] == -1:
            print("Not Found")
        else:
            print("Match Found \nRegsiter id : ", res[0])