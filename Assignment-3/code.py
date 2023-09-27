import RPi.GPIO as GPIO
import time
from pyrebase import initialize_app

# Initialize Firebase
config = {
  'apiKey': "",
  'authDomain': "",
  'databaseURL': "",
  'projectId': "",
  'storageBucket': "",
  'messagingSenderId': "",
  'appId': "",
  'measurementId': ""
}

firebase = initialize_app(config)
db = firebase.database()

pir_sensor = 11
piezo = 7

GPIO.setmode(GPIO.BOARD)

GPIO.setup(piezo, GPIO.OUT)

GPIO.setup(pir_sensor, GPIO.IN)

current_state = 0 

try:
    while True:
        time.sleep(0.1)
        current_state = GPIO.input(pir_sensor)
        if current_state == 1:
            print("GPIO pin %s is %s" % (pir_sensor, current_state))
            GPIO.output(piezo, True)
            time.sleep(1)
            GPIO.output(piezo, False)
            time.sleep(5)
            # Push data to Firebase
            db.child("motion").push({"status": "detected"})
        else:
            print("GPIO pin %s is %s" % (pir_sensor, current_state))
            # Push data to Firebase
            db.child("motion").push({"status": "not detected"})

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
