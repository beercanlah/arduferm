import numpy as np
import matplotlib.pyplot as plt

resolution = 1024.0
adc_max = 5
resistor = 10e3
bridge_voltage = 5
adc = np.arange(0, resolution)
measured_voltage = adc_max * adc / resolution

therm_resistance = np.divide(resistor * measured_voltage,
                             bridge_voltage - measured_voltage)

print therm_resistance[np.argmin(np.abs(measured_voltage - 1.6))]

print therm_resistance
upper_found = False
for k in range(len(therm_resistance)):
    # Find zero degree point by comparing resistance to value in data sheet
    #110 deg - 511
    # 40 deg - 5327
    # 30 deg - 8057
    # 20 deg - 12490
    #  0 deg - 32650
    # -5 deg - 42315
    if therm_resistance[k] > 511 and not upper_found:
        upper_point = k
        upper_found = True

    if therm_resistance[k] > 32650:
        lower_point = k
        break

index = slice(upper_point, lower_point + 1)

adc = adc[index]
therm_resistance = therm_resistance[index]

R0 = 10e3
T0 = 298.15
B = 3988
Rinf = R0 * np.exp(-B / T0)

T = B / np.log(therm_resistance / Rinf) - 273.15

# Slice again now that we now temperature
condition = np.logical_and(T >= 0, T <= 110)
T = T[condition]
adc = adc[condition]

T_round = np.round(10 * T)
pos = np.arange(0, len(adc))

table = np.vstack([adc, T_round])
table = table.astype('int')
np.savetxt('temp_table_compressor.csv', table, delimiter=',', fmt='%d')
plt.plot(adc, T)
plt.show()
