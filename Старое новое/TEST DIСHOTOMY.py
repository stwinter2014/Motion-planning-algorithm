from math import floor
from decimal import Decimal
import Interpolation
import AccDecControl
import Graphs

#input data
move_type = [0]    #type of trajectory for each block (0 - linear, 1 - circular, 2 - curve)
trajectory = [[0,0], [10, 10], [10, 9.5], [15, 10], [16, 13], [16, 18]]   #trajectory points
feedrate = [50, 80, 25, 25, 25]     #list of feedrates for each block
feedrate_max = [60, 75, 60, 50, 60]
acceleration = [500, 500, 30, 30, 5000] #allowable acceleration for each block
deceleration = [5000, 5000, 5000, 5000, 5000] #allowable deceleration for each block
jerk = [5000, 5000, 50000, 50000, 50000]
#период интерполяции
tsample = Decimal(0.004).quantize(Decimal("1.0000"))
#tolerance
linearErr = Decimal(0.001).quantize(Decimal("1.0000"))
radiusErr = Decimal(0.005).quantize(Decimal("1.0000"))
#corner parameters

velocity_list = []

for i in range (1,2):
    #расчет длины пути
    blocklen = Decimal(Interpolation.LengthLinear(trajectory[i], trajectory[i+1])).quantize(Decimal("1.0000"))
    print("Участок " + str(i+1) + ". Длина пути: " + str(blocklen) + " мм.")

    #предварительный расчет длины разгона и торможения
    Nm = floor(acceleration[i]/(jerk[i]*tsample))

    LengthAcc = AccDecControl.AccDecDisplacement (4, feedrate[i], jerk[i], acceleration[i], tsample, Nm)
    LengthDec = AccDecControl.AccDecDisplacement (feedrate[i], 5, jerk[i], acceleration[i], tsample, Nm)
    print("     Длина разгона: " + str(LengthAcc) + " мм.")
    print("     Длина торможения: " + str(LengthDec) + " мм.")

    #расчет реальной максимальной скорости
    MaxFeedrate = AccDecControl.RealMaxFeedrate (4, 5, feedrate[i], blocklen, Nm, LengthAcc, LengthDec, linearErr, jerk[i], acceleration[i], tsample)
    print("     Макс. скорость: " + str(MaxFeedrate[0]) + " мм/c.")
    #print("Длина разгона и торможения: " + str(MaxFeedrate[1]) + " мм.")

    #построение профиля скорости
    Profile = AccDecControl.AccDecType (4, 5, MaxFeedrate[0], blocklen, jerk[i], acceleration[i], tsample, Nm)
    velocity_list += Profile[0]+Profile[1]+Profile[2]

#вывод графического материала
timelist = []
time = 0
for i in range (len(velocity_list)):
    time += tsample
    timelist.append(time)
Graphs.Graph_01 (timelist, velocity_list,
                 'Время, с', 'Скорость, мм/с', 'Профиль скорости', 'Скорость инструмента')

