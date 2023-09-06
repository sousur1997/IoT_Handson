from adafruit_ble.uuid import StandardUUID, VendorUUID
from adafruit_ble.characteristics import Characteristic
from adafruit_ble.attributes import Attribute
from adafruit_ble.services import Service
from adafruit_ble.characteristics.int import Uint16Characteristic, Uint8Characteristic
from adafruit_ble.characteristics.float import FloatCharacteristic
from adafruit_ble.characteristics.string import StringCharacteristic
from adafruit_ble_adafruit.adafruit_service import AdafruitService

class Environment_Service(AdafruitService):
    uuid = StandardUUID(0x181A) # VendorUUID("1f4e1ef3-39b0-4253-ab1c-82ebeeda087d")

    temperature = Uint16Characteristic(
        uuid = StandardUUID(0x2A6E), #VendorUUID("1f4e1ef3-39b0-4253-ab1c-82ebeeda087e"),
        properties = (Characteristic.READ | Characteristic.NOTIFY),
        write_perm=Attribute.OPEN,
        read_perm=Attribute.OPEN,
    )

    message = StringCharacteristic(
        uuid = VendorUUID("a118902b-547e-4619-915a-c66bda7949ca"),
        properties = (Characteristic.READ | Characteristic.WRITE | Characteristic.NOTIFY),
        write_perm=Attribute.OPEN,
        read_perm=Attribute.OPEN,
    )


