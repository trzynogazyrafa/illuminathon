import time
import board
import adafruit_mpu6050
import busio
import digitalio
from displayio import Group, TileGrid, Bitmap, Palette
from adafruit_display_text import bitmap_label as label
import terminalio
from foamyguy_waveshare_pico_lcd_1_14 import WavesharePicoLCD114

# Initialize I2C and MPU6050
i2c = busio.I2C(board.GP27, board.GP26)
mpu = adafruit_mpu6050.MPU6050(i2c)

# Set up the display
lcd = WavesharePicoLCD114()
display = lcd.display
main_group = Group()

# Background color setup
BORDER = 10
BACKGROUND_COLOR = 0x00FF00
FOREGROUND_COLOR = 0xAA0088
TEXT_COLOR = 0xFFFFFF

# Create background and inner rectangle
color_bitmap = Bitmap(display.width, display.height, 1)
color_palette = Palette(1)
color_palette[0] = BACKGROUND_COLOR
bg_sprite = TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
main_group.append(bg_sprite)

inner_bitmap = Bitmap(display.width - BORDER * 2, display.height - BORDER * 2, 1)
inner_palette = Palette(1)
inner_palette[0] = FOREGROUND_COLOR
inner_sprite = TileGrid(inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER)
main_group.append(inner_sprite)

# Create text labels for sensor data
text_group = Group(scale=1, x=10, y=10)
accel_label = label.Label(terminalio.FONT, text="Accel: ", color=TEXT_COLOR)
gyro_label = label.Label(terminalio.FONT, text="Gyro: ", color=TEXT_COLOR, y=20)
temp_label = label.Label(terminalio.FONT, text="Temp: ", color=TEXT_COLOR, y=40)
text_group.append(accel_label)
text_group.append(gyro_label)
text_group.append(temp_label)

main_group.append(text_group)
display.root_group = main_group

# Main loop to update display with sensor data
while True:
    accel = mpu.acceleration
    gyro = mpu.gyro
    temp = mpu.temperature
    
    accel_label.text = "Accel: X=%.2f Y=%.2f Z=%.2f" % accel
    gyro_label.text = "Gyro: X=%.2f Y=%.2f Z=%.2f" % gyro
    temp_label.text = "Temp: %.2f C" % temp
    
    time.sleep(1)
