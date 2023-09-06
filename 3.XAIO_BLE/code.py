from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
import _bleio
import adafruit_ble
import time
import board, digitalio
from gatt_services import Environment_Service
import microcontroller

BLINK_DURATION = 0.25
TOTAL_BLINK = 2
BLINK_COUNT_CONNECT = [0]   # list to act as reference variable
BLINK_COUNT_DISCONNECT = [0]
WAS_CONNECTED = False   # to check BLE client was connected previously or not

# set RED and GREEN led as output
red_led = digitalio.DigitalInOut(board.LED_RED)
red_led.direction = digitalio.Direction.OUTPUT
red_led.value = True

green_led = digitalio.DigitalInOut(board.LED_GREEN)
green_led.direction = digitalio.Direction.OUTPUT
green_led.value = True

def ble_blink(led_pin, blink_count):
    while blink_count[0] < TOTAL_BLINK * 2:
        led_pin.value = not led_pin.value
        time.sleep(BLINK_DURATION)
        blink_count[0] += 1
    led_pin.value = True

radio = adafruit_ble.BLERadio()
env_service = Environment_Service()

adv = ProvideServicesAdvertisement(env_service)
adv.complete_name = "Air Sense"
adv.appearance = 1346

while True:
    if not radio.connected:
        BLINK_COUNT_CONNECT[0] = 0
        if WAS_CONNECTED:
            ble_blink(red_led, BLINK_COUNT_DISCONNECT)
            WAS_CONNECTED = False

        try:
            radio.start_advertising(adv)
        except _bleio.BluetoothError as e:  # may cause Already advertising error
            pass

    if radio.connected:
        conn = radio.connections[0]

        # blink to indicate BLE is connected
        ble_blink(green_led, BLINK_COUNT_CONNECT)
        BLINK_COUNT_DISCONNECT[0] = 0   # reset counter to blink when disconnect again
        WAS_CONNECTED = True

        radio.stop_advertising()

    temp = microcontroller.cpu.temperature

    print("Temperature: %0.1f *C" % temp)

    msg = env_service.message
    env_service.temperature = int(temp)

    print("Received Message:", msg)

    time.sleep(5)
