from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)

for i in range(10):
    led.toggle()

    print(f"BioLoop-Pi Pico check: {i + 1}")

    sleep(0.5)

led.off()

print("Pico 2 W hardware check complete.")