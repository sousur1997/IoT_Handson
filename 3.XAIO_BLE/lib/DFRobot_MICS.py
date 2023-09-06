import time
'''
 * @file DFRobot_MICS.h
 * @brief Define the basic structure of class DFRobot_MicsSensor
 * @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license The MIT License (MIT)
 * @author [ZhixinLiu](zhixin.liu@dfrobot.com)
 * @version V1.1
 * @date 2020-4-20
 * @url https://github.com/DFRobot/DFRobot_MICS
'''

MICS_ADDRESS_0 = 0x75
MICS_ADDRESS_1 = 0x76
MICS_ADDRESS_2 = 0x77
MICS_ADDRESS_3 = 0x78

ERROR = -1
OX_MODE = 0x00
RED_MODE = 0x01

OX_REGISTER_HIGH = 0x04
OX_REGISTER_LOW = 0x05
RED_REGISTER_HIGH = 0x06
RED_REGISTER_LOW = 0x07
POWER_REGISTER_HIGH = 0x08
POWER_REGISTER_LOW = 0x09
POWER_MODE_REGISTER = 0x0a

SLEEP_MODE = 0x00
WAKE_UP_MODE = 0x01

EXIST = 0x00
NO_EXIST = 0x02

CO = 0x01          # Carbon Monoxide
CH4 = 0x02          # Methane
C2H5OH = 0x03          # Ethanol
C3H8 = 0x04          # Propane
C4H10 = 0x05          # Iso Butane
H2 = 0x06          # Hydrogen
H2S = 0x07          # Hydrothion
NH3 = 0x08          # Ammonia
NO = 0x09          # Nitric Oxide
NO2 = 0x0A          # Nitrogen Dioxide


class DFRobot_MICS:

	__r0_ox = 0
	__r0_red = 0
	__nowTime = 0
	__flag = 0

	def __init__(self):	# empty constructor
		pass

	def warmUpTime(self, minute):
		oxData = bytearray(1)
		redData = bytearray(1)
		powerData = bytearray(1)
		delayTime = 0
		excessTime = 0

		if self.__flag == 0:
			self.__flag = 1
			self.__nowTime = time.time()
			
		delayTime = minute * 60
		excessTime = time.time() - self.__nowTime
		if excessTime < delayTime:
			return False
		
		if self.__getSensorData(oxData, redData, powerData) == ERROR:
			return False
		
		self.__r0_ox = powerData[0] - oxData[0]
		self.__r0_red = powerData[0] - redData[0]
		return True

	def getADCData(self, mode):
		oxData = bytearray(1)
		redData = bytearray(1)
		powerData = bytearray(1)
		RS_R0_RED_data = 0
		RS_R0_OX_data = 0

		self.__getSensorData(oxData, redData, powerData)
		if powerData[0] <= redData[0]:
			RS_R0_RED_data = 0
		else:
			RS_R0_RED_data = (powerData[0] - redData[0])

		if powerData[0] <= oxData[0]:
			RS_R0_OX_data = 0
		else:
			RS_R0_OX_data = (powerData[0] - oxData[0])

		if mode == OX_MODE:
			return RS_R0_OX_data
		else:
			return RS_R0_RED_data


	def getGasData(self, type):
		oxData = bytearray(1)
		redData = bytearray(1)
		powerData = bytearray(1)

		self.__getSensorData(oxData, redData, powerData)

		RS_R0_RED_data = (powerData[0] - redData[0]) / self.__r0_red
		RS_R0_OX_data = (powerData[0] - oxData[0]) / self.__r0_ox

		if type == CO:
			return self.__getCarbonMonoxide(RS_R0_RED_data)
		elif type == CH4:
			return self.__getMethane(RS_R0_RED_data)
		elif type == C2H5OH:
			return self.__getEthanol(RS_R0_RED_data)
		elif type == H2:
			return self.__getHydrogen(RS_R0_RED_data)
		elif type == NH3:
			return self.__getAmmonia(RS_R0_RED_data)
		elif type == NO2:
			return self.__getNitrogenDioxide(RS_R0_OX_data)
		else:
			return ERROR

	def getGasExist(self, gas):
		oxData = bytearray(1)
		redData = bytearray(1)
		powerData = bytearray(1)

		self.__getSensorData(oxData, redData, powerData)

		RS_R0_RED_data = (powerData[0] - redData[0]) / self.__r0_red
		RS_R0_OX_data = (powerData[0] - oxData[0]) / self.__r0_ox

		if gas == C3H8:
			if self.__existPropane(RS_R0_RED_data):
				return EXIST
			else:
				return NO_EXIST
		elif gas == C4H10:
			if self.__existIsoButane(RS_R0_RED_data):
				return EXIST
			else:
				return NO_EXIST
		elif gas == H2S:
			if self.__existHydrothion(RS_R0_RED_data):
				return EXIST
			else:
				return NO_EXIST
		elif gas == NO:
			if self.__existNitricOxide(RS_R0_RED_data):
				return EXIST
			else:
				return NO_EXIST
		elif gas == CO:
			if self.__existCarbonMonoxide(RS_R0_RED_data):
				return EXIST
			else:
				return NO_EXIST
		elif gas == CH4:
			if self.__existMethane(RS_R0_RED_data):
				return EXIST
			else:
				return NO_EXIST
		elif gas == C2H5OH:
			if self.__existEthanol(RS_R0_RED_data):
				return EXIST
			else:
				return NO_EXIST
		elif gas == H2:
			if self.__existHydrogen(RS_R0_RED_data):
				return EXIST
			else:
				return NO_EXIST
		elif gas == NH3:
			if self.__existAmmonia(RS_R0_RED_data):
				return EXIST
			else:
				return NO_EXIST
		elif gas == NO2:
			if self.__existNitrogenDioxide(RS_R0_OX_data):
				return EXIST
			else:
				return NO_EXIST
		else:
			return ERROR

	def sleepMode(self):
		regData = bytearray([SLEEP_MODE])
		self.writeData(POWER_MODE_REGISTER, regData, 1)
		time.sleep(0.1)

	def wakeUpMode(self):
		regData = bytearray([WAKE_UP_MODE])
		self.writeData(POWER_MODE_REGISTER, regData, 1)
		time.sleep(0.1)

	def getPowerState(self):
		regData = bytearray(1)
		self.readData(POWER_MODE_REGISTER, regData, 1)
		return regData

	# def writeData(self, reg, data, length):	# data must be mutable
	# 	pass

	# def readData(self, reg, data, length):	# data must be mutable
	# 	pass

	def __getSensorData(self, oxData, redData, powerData):
		recv_data = bytearray(20)
		self.readData(OX_REGISTER_HIGH, recv_data, 6)
		oxData[0] = ((recv_data[0] << 8) | recv_data[1]) & 0xFF
		redData[0] = ((recv_data[2] << 8) | recv_data[3]) & 0xFF
		powerData[0] = ((recv_data[4] << 8) | recv_data[5]) & 0xFF
		return 0

	def __getCarbonMonoxide(self, data):
		if data > 0.425:
			return 0.0
		co = (0.425 - data) / 0.000405
		if co > 1000.0:
			return 1000.0
		if co < 1.0:
			return 0.0
		return co

	def __getMethane(self, data):
		if data > 0.786:
			return 0.0
		methane = (0.786 - data) / 0.000023
		if methane < 1000.0:
			return 0.0
		if methane > 25000.0:
			return 25000.0
		return methane

	def __getEthanol(self, data):
		if data > 0.306:
			return 0.0
		ethanol = (0.306 - data) / 0.00057
		if ethanol < 10.0:
			return 0.0
		if ethanol > 500.0:
			return 500.0
		return ethanol

	def __getHydrogen(self, data):
		if data > 0.279:
			return 0.0
		hydrogen = (0.279 - data) / 0.00026
		if hydrogen < 1.0:
			return 0.0
		if hydrogen > 1000.0:
			return 1000.0
		return hydrogen

	def __getAmmonia(self, data):
		if data > 0.8:
			return 0.0
		ammonia = (0.8 - data) / 0.0015
		if ammonia < 1.0:
			return 0.0
		if ammonia > 500.0:
			return 500.0
		return ammonia
	
	def __getNitrogenDioxide(self, data):
		if data < 1.1:
			return 0.0
		nitrogendioxide = (data - 0.045) / 6.13
		if nitrogendioxide < 0.1:
			return 0.0
		if nitrogendioxide > 10.0:
			return 10.0
		return nitrogendioxide
	
	def __existPropane(self, data):
		if data > 0.18:
			return False
		return True
	
	def __existNitricOxide(self, data):
		if data > 0.8:
			return False
		return True
	
	def __existIsoButane(self, data):
		if data > 0.65:
			return False
		return True
	
	def __existHydrothion(self, data):
		if data > 0.58 and data < 0.69:
			return True
		if data < 0.201:
			return True
		return False
	
	def __existCarbonMonoxide(self, data):
		if data > 0.425:
			return False
		return True
	
	def __existMethane(self, data):
		if data > 0.786:
			return False
		return True
	
	def __existEthanol(self, data):
		if data > 0.306:
			return False
		return True
	
	def __existHydrogen(self, data):
		if data > 0.279:
			return False
		return True
	
	def __existAmmonia(self, data):
		if data < 1.1:
			return False
		return True
	
	def __existNitrogenDioxide(self, data):
		if data > 0.65:
			return False
		return True
	

class DFRobot_MICS_I2C(DFRobot_MICS):
	
	def __init__(self, i2c, addr = MICS_ADDRESS_0):
		self.__i2c = i2c
		self.__addr = addr

	def writeData(self, reg, data, length):	# data must be mutable
		while not self.__i2c.try_lock():
			pass
		try:
			self.__i2c.writeto(self.__addr, bytearray([reg]))
			self.__i2c.writeto(self.__addr, data)
		finally:
			self.__i2c.unlock()

	def readData(self, reg, data, length):	# data must be mutable
		while not self.__i2c.try_lock():
			pass
		try:
			self.__i2c.writeto(self.__addr, bytearray([reg]))
			time.sleep(0.01)

			self.__i2c.readfrom_into(self.__addr, data)
		finally:
			self.__i2c.unlock()
