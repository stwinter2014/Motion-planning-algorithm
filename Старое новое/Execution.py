from math import floor
from decimal import Decimal
import Interpolation
import AccDecControl
import Graphs

#input data
move_type = [0]    #type of trajectory for each block (0 - linear, 1 - circular, 2 - curve)
trajectory = [[0,0], [10, 10], [10, 9.5], [15, 10], [16, 13], [16, 18]]   #trajectory points
feedrate = [100, 80, 100, 100, 100]     #list of feedrates for each block
feedrate_max = [60, 75, 60, 50, 60]
acceleration = [5000, 5000, 5000, 5000, 5000] #allowable acceleration for each block
deceleration = [5000, 5000, 5000, 5000, 5000] #allowable deceleration for each block
jerk = [50000, 50000, 50000, 50000, 50000]
#период интерполяции
tsample = Decimal(0.004).quantize(Decimal("1.0000"))
#tolerance
linearErr = Decimal(0.001).quantize(Decimal("1.0000"))
radiusErr = Decimal(0.005).quantize(Decimal("1.0000"))
#corner parameters

velocity_list = []
"""
for i in range (0,2):
    #расчет длины пути
    blocklen = Decimal(Interpolation.LengthLinear(trajectory[i], trajectory[i+1])).quantize(Decimal("1.0000"))
    print("Участок " + str(i+1) + ". Длина пути: " + str(blocklen) + " мм.")

    #предварительный расчет длины разгона и торможения
    Nm = floor(acceleration[i]/(jerk[i]*tsample))

    LengthAcc = AccDecControl.AccDecDisplacement (4, feedrate[i], jerk[i], acceleration[i], tsample, Nm)
    LengthDec = AccDecControl.AccDecDisplacement (feedrate[i], 5, jerk[i], acceleration[i], tsample, Nm)
    print("Предварительная длина разгона: " + str(LengthAcc) + " мм.")
    print("Предварительная длина торможения: " + str(LengthDec) + " мм.")

    #расчет реальной максимальной скорости
    MaxFeedrate = AccDecControl.RealMaxFeedrate (4, 5, feedrate[i], blocklen, Nm, LengthAcc, LengthDec, linearErr, jerk[i], acceleration[i], tsample)
    print("Максимальная скорость сегмента: " + str(MaxFeedrate[0]) + " мм/c.")
    #print("Длина разгона и торможения: " + str(MaxFeedrate[1]) + " мм.")

    #построение профиля скорости
    Profile = AccDecControl.AccDecType (0, 0, MaxFeedrate[0], blocklen, jerk[i], acceleration[i], tsample, Nm)
    velocity_list += Profile[0]+Profile[1]+Profile[2]
"""
"""
#вывод графического материала
timelist = []
time = 0
for i in range (len(velocity_list)):
    time += tsample
    timelist.append(time)
Graphs.Graph_01 (timelist, velocity_list,
                 'Время, с', 'Скорость, мм/с', 'Профиль скорости', 'Скорость инструмента')

"""
N = Nt = 3
blocklen_list = []
Vs = 0
Ve = 0
#РАСЧЕТ ДЛИН УЧАСТКОВ
for i in range (len(feedrate)):
    Nm = floor(acceleration[i]/(jerk[i]*tsample))
    blocklen = Decimal(Interpolation.LengthLinear(trajectory[i], trajectory[i+1])).quantize(Decimal("1.0000"))
    blocklen_list.append(blocklen)
for i in range (len(feedrate)):
    #РАСЧЕТ ГРАНИЧНОЙ СКОРОСТИ ТЕКУЩЕГО УЧАСТКА
    if len(feedrate) - len(feedrate[0:i]) < N:
        Nt -=1
    print("Участок " + str(i))
    print(Nt)
    print("Длина пути участка " + str(i+1) + ": " + str(blocklen_list[i]) + " мм.")
    print(feedrate[i:i+Nt])
    Vend_i = AccDecControl.LinkedFeedrate (Ve, blocklen_list[i:i+Nt], feedrate[i:i+Nt], Nm, feedrate_max[i:i+Nt], Nt, jerk[0], acceleration[0], tsample, linearErr)
    Ve = Vend_i
    print("Граничная скорость: " + str(Vend_i))
    
    #РАСЧЕТ ПРОФИЛЯ ТЕКУЩЕГО УЧАСТКА
    #предварительный расчет длины разгона и торможения
    LengthAcc = AccDecControl.AccDecDisplacement (Vs, feedrate[i], jerk[i], acceleration[i], tsample, Nm)
    LengthDec = AccDecControl.AccDecDisplacement (feedrate[i], Ve, jerk[i], acceleration[i], tsample, Nm)
    print("Предварительная длина разгона: " + str(LengthAcc) + " мм.")
    print("Предварительная длина торможения: " + str(LengthDec) + " мм.")

    #расчет реальной максимальной скорости
    MaxFeedrate = AccDecControl.RealMaxFeedrate (Vs, Ve, feedrate[i], blocklen_list[i], Nm, LengthAcc, LengthDec, linearErr, jerk[i], acceleration[i], tsample)
    print("Максимальная скорость сегмента: " + str(MaxFeedrate[0]) + " мм/c.")
    #print("Длина разгона и торможения: " + str(MaxFeedrate[1]) + " мм.")

    #построение профиля скорости
    Profile = AccDecControl.AccDecType (Vs, Ve, MaxFeedrate[0], blocklen_list[i], jerk[i], acceleration[i], tsample, Nm)
    velocity_list += Profile[0]+Profile[1]+Profile[2]
    Vs = Ve
    print("_________________________________________________________________")
#вывод графического материала
timelist = []
time = 0
for i in range (len(velocity_list)):
    time += tsample
    timelist.append(time)
Graphs.Graph_01 (timelist, velocity_list,
                 'Время, с', 'Скорость, мм/с', 'Профиль скорости', 'Скорость инструмента')
