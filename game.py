# 主循環首先產生一個1到9之間的隨機數，並點亮對應的燈。
# 然後進入一個循環，等待按鍵輸入。
# 當偵測到按鍵輸入時，檢查按鍵是否與隨機產生的數字相符。
# 如果按鍵正確，呼叫clear_display清除顯示。
# 如果按鍵錯誤，呼叫show_error顯示錯誤提示。
# 循環重複，繼續產生下一個隨機數字並偵測按鍵輸入。
import RPi.GPIO as GPIO
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from time import sleep
import random
import db_insert

# Define GPIO pins for keypad
L1, L2, L3, L4 = 5, 6, 13, 19
C1, C2, C3, C4 = 1, 12, 20, 21

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Define SPI interface and LED matrix
CS_PIN = 8  # Replace with your actual CS pin
BLOCK_NUM = 1  # Replace with your block number
HEIGHT = 8
WIDTH = 8 * BLOCK_NUM

serial = spi(port=0, device=0, gpio=noop(), cs=CS_PIN)
device = max7219(serial, cascaded=BLOCK_NUM, block_orientation=-90)

def start_timer():
    return time.time()

def stop_timer(start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

def clear_display():
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="black", fill="black")
    sleep(0.1)

def light_pixels_for_number(number):
    with canvas(device) as draw:
        if number == 1:
            pixels = [(0, 6), (0, 7), (1, 6), (1, 7)]
        elif number == 2:
            pixels = [(0, 3), (0, 4), (1, 3), (1, 4)]
        elif number == 3:
            pixels = [(0, 0), (0, 1), (1, 0), (1, 1)]
        elif number == 4:
            pixels = [(3, 6), (3, 7), (4, 6), (4, 7)]
        elif number == 5:
            pixels = [(3, 3), (3, 4), (4, 3), (4, 4)]
        elif number == 6:
            pixels = [(3, 0), (3, 1), (4, 0), (4, 1)]
        elif number == 7:
            pixels = [(6, 6), (6, 7), (7, 6), (7, 7)]
        elif number == 8:
            pixels = [(6, 3), (6, 4), (7, 3), (7, 4)]
        elif number == 9:
            pixels = [(6, 0), (6, 1), (7, 0), (7, 1)]
        else:
            pixels = []

        for pixel in pixels:
            draw.point(pixel, fill="white")

def show_error():
    with canvas(device) as draw:
        pixels = [
            (0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
            (0, 7), (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0)
        ]
        for pixel in pixels:
            draw.point(pixel, fill="white")
    sleep(2)

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    if GPIO.input(C1) == 1:
        return characters[0]
    if GPIO.input(C2) == 1:
        return characters[1]
    if GPIO.input(C3) == 1:
        return characters[2]
    if GPIO.input(C4) == 1:
        return characters[3]
    GPIO.output(line, GPIO.LOW)
    return None

def wait_for_start():
    print("Press '0' to start the game.")
    light_border_pixels()
    while True:
        for line, characters in [(L1, ["1", "2", "3", "A"]),
                                 (L2, ["4", "5", "6", "B"]),
                                 (L3, ["7", "8", "9", "C"]),
                                 (L4, ["*", "0", "#", "D"])]:
            if readLine(line, characters) == "0":
                clear_display()
                return
            if readLine(line, characters) == "*":
                clear_display()
                print("Press '#' to open the light.")
            if readLine(line, characters) == "#":
                light_border_pixels()
                print("Press '*' to close the light.")
        time.sleep(0.1)  # Small delay to debounce

def light_all_pixels():
    with canvas(device) as draw:
        for x in range(8):
            for y in range(8):
                draw.point((x, y), fill="white")
                
def light_border_pixels():
    with canvas(device) as draw:
        for x in range(8):
            draw.point((x, 0), fill="white")
            draw.point((x, 7), fill="white")
        for y in range(8):
            draw.point((0, y), fill="white")
            draw.point((7, y), fill="white")
        
def select_user():
    light_all_pixels()
    user_names = {"A": "user_A", "B": "user_B", "C": "user_C", "D": "user_D"}
    usr_name = None
    while not usr_name:
        for line, characters in [(L1, ["1", "2", "3", "A"]),
                                 (L2, ["4", "5", "6", "B"]),
                                 (L3, ["7", "8", "9", "C"]),
                                 (L4, ["*", "0", "#", "D"])]:
            pressed_key = readLine(line, characters)
            if pressed_key in user_names:
                usr_name = user_names[pressed_key]
                print(f"User selected: {usr_name}")
                clear_display()
                break
        time.sleep(0.1)  # Small delay to debounce
    return usr_name        
        
def game_loop():
    print("Timer started.")
    start_time = start_timer()
    random_numbers = []
    for _ in range(5):
        random_number = random.randint(1, 9)
        random_numbers.append(random_number)
        clear_display()
        
        for index, number in enumerate(random_numbers):
            clear_display()
            light_pixels_for_number(number)
            print("output" + str(number))
            sleep(1)

        correct_inputs = 0
        while correct_inputs < len(random_numbers):
            pressed_key = None
            while not pressed_key:
                for line, characters in [(L1, ["1", "2", "3", "A"]),
                                         (L2, ["4", "5", "6", "B"]),
                                         (L3, ["7", "8", "9", "C"]),
                                         (L4, ["*", "0", "#", "D"])]:
                    pressed_key = readLine(line, characters)
                    if pressed_key:
                        print("input" + pressed_key)
                        break
                time.sleep(0.1)  # Small delay to debounce

            if pressed_key == str(random_numbers[correct_inputs]):
                correct_inputs += 1
                clear_display()
            else:
                show_error()
                clear_display()
                print("\nIncorrect input. Program terminating.")
                return

    elapsed_time = stop_timer(start_time)
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    user_names = {"A": "user_A", "B": "user_B", "C": "user_C", "D": "user_D"}
    usr_name = None
    while not usr_name:
        for line, characters in [(L1, ["1", "2", "3", "A"]),
                                 (L2, ["4", "5", "6", "B"]),
                                 (L3, ["7", "8", "9", "C"]),
                                 (L4, ["*", "0", "#", "D"])]:
            pressed_key = readLine(line, characters)
            if pressed_key in user_names:
                usr_name = user_names[pressed_key]
                print(f"User selected: {usr_name}")
                break
        time.sleep(0.1)  # Small delay to debounce

    db_insert.upload_to_sql(usr_name, elapsed_time)

try:
    while True:
        wait_for_start()
        game_loop()    
    
except KeyboardInterrupt:
    print("\nAPP stopped!")
finally:
    device.cleanup()
    GPIO.cleanup()
