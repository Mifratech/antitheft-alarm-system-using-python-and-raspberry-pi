import cv2
import datetime
import RPi.GPIO as GPIO
import time
import requests

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# setup PWM process
servo_pin = 23
GPIO.setup(servo_pin,GPIO.OUT)
pwm = GPIO.PWM(servo_pin,50) # 50 Hz (20 ms PWM period)
pwm.start(3)

input1 = 21
input2 = 20
input3 = 16
input4 = 12

GPIO.setup(input1 ,GPIO.IN ,pull_up_down=GPIO.PUD_UP) #input 1 pin number
GPIO.setup(input2 ,GPIO.IN ,pull_up_down=GPIO.PUD_UP) #input 2 pin number
GPIO.setup(input3 ,GPIO.IN ,pull_up_down=GPIO.PUD_UP) #input 3 pin number
GPIO.setup(input4 ,GPIO.IN ,pull_up_down=GPIO.PUD_UP) #input 4 pin number

body = "Alert Person Detected"
toaddr = "abnabi143@gmail.com"

def send_mail():
    try:
        global body
        global toaddr
        global filename
        print("Sending Mail Please Wait")
        myfile = "captured_images/"+ filename + ".jpg"
        url = "http://esp-sms.000webhostapp.com/mail.php?email="+toaddr+"&msg="+body
        files = {'image': open(myfile, 'rb')}
        r = requests.post(url, files=files, verify=False,timeout=8)
        print(r.status_code)
    except:
        print("Internet Error")

print(datetime.datetime.now())
img = cv2.VideoCapture(0)
time.sleep(1)
counter = 0

while True:
    ret,frame = img.read()
    val1 = GPIO.input(input1) #reading input 1 val
    val2 = GPIO.input(input2) #reading input 1 val
    val3 = GPIO.input(input3) #reading input 1 val
    val4 = GPIO.input(input4) #reading input 1 val
    
    print("input 1 value:",val1)
    print("input 2 value:",val2)
    print("input 3 value:",val3)
    print("input 4 value:",val4)
    
    if val1 == 0:
        pwm.ChangeDutyCycle(3)
        filename = str(datetime.datetime.now())
        cv2.imwrite("captured_images/"+ filename + ".jpg",frame)
        send_mail()
        print("sent")
        
    elif val2 == 0:
        pwm.ChangeDutyCycle(6)
        filename = str(datetime.datetime.now())
        cv2.imwrite("captured_images/"+ filename + ".jpg",frame)
        send_mail()
        print("sent")
        
    elif val3 == 0:
        pwm.ChangeDutyCycle(9)
        filename = str(datetime.datetime.now())
        cv2.imwrite("captured_images/"+ filename + ".jpg",frame)
        send_mail()
        print("sent")
        
    elif val4 == 0:
        pwm.ChangeDutyCycle(12)
        filename = str(datetime.datetime.now())
        cv2.imwrite("captured_images/"+ filename + ".jpg",frame)
        send_mail()
        print("sent")
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.1)

img.release()
