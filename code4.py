import time
import board
import adafruit_mpu6050
import busio
from displayio import Group, TileGrid, Bitmap, Palette
from foamyguy_waveshare_pico_lcd_1_14 import WavesharePicoLCD114

# Initialize I2C and MPU6050
i2c = busio.I2C(board.GP27, board.GP26)  
mpu = adafruit_mpu6050.MPU6050(i2c)

# Set up the display
lcd = WavesharePicoLCD114()
display = lcd.display
main_group = Group()

# Background setup
BACKGROUND_COLOR = 0x000000  # Black background
PIXEL_COLOR = 0xFFFF00  # Yellow pixel

# Create background
color_bitmap = Bitmap(display.width, display.height, 1)
#print(display.width, display.height)
color_palette = Palette(1)
color_palette[0] = BACKGROUND_COLOR
bg_sprite = TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
main_group.append(bg_sprite)

# Create pixel bitmap (1x1 size) for movement
pixel_bitmap = Bitmap(1, 1, 1)
pixel_palette = Palette(1)
pixel_palette[0] = PIXEL_COLOR
pixel_sprite = TileGrid(pixel_bitmap, pixel_shader=pixel_palette, x=display.width // 2, y=display.height // 2)
main_group.append(pixel_sprite)

display.root_group = main_group

# Variables to track pixel position
x_pos = display.width // 2
y_pos = display.height // 2

# Sensitivity for movement (higher = less sensitive)
sensitivity = 5

# Main loop to update pixel position based on MPU6050 data
while True:
    # Get acceleration data
    accel_x, accel_y, accel_z = mpu.acceleration
    print(accel_x, accel_y, accel_z)
    # Map acceleration to movement on screen
    x_pos += int(accel_x * sensitivity)
    y_pos += int(accel_y * sensitivity)
    
    # Ensure the pixel stays within screen bounds
    x_pos = max(0, min(display.width - 1, x_pos))
    y_pos = max(0, min(display.height - 1, y_pos))
    
    # Update pixel position
    pixel_sprite.x = x_pos
    pixel_sprite.y = y_pos
    print(x_pos, y_pos)
    # Small delay to control update speed
    time.sleep(0.5)
