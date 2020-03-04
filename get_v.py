import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1015(i2c)


#Single Ended Mode
# chan = AnalogIn(ads, ADS.P0)
chan = AnalogIn(ads, ADS.P1)
print(chan.value, "%.2f" % chan.voltage)


adj = float(chan.voltage)/0.09
#print("adj: " + str(adj) )
print("adj: %.2f Volt" % adj )
# Differential Mode
# chan = AnalogIn(ads, ADS.P0, ADS.P1)
# print(chan.value, chan.voltage)

