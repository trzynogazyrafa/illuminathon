import time
import board
import adafruit_mpu6050
import busio
import digitalio

#scl_pin=digitalio.DigitalInOut(board.GP15)
#sda_pin=digitalio.DigitalInOut(board.GP14)
i2c = busio.I2C(board.GP15, board.GP14) # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(mpu.gyro))
    print("Temperature: %.2f C"%mpu.temperature)
    print("")
    time.sleep(1)