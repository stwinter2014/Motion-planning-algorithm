from math import floor
import Interpolation
import AccDecControl
import Graphs
from decimal import Decimal

#input data
move_type = [0]    #type of trajectory for each block (0 - linear, 1 - circular, 2 - curve)
trajectory = [[0,0], [100, 100], [100, 90], [100, 0]]   #trajectory points
feedrate = [30, 25, 30]     #list of feedrates for each block
#feedrate_max = [30, 30, 30]
acceleration = [25, 25, 25] #allowable acceleration for each block
deceleration = [25, 25, 25] #allowable deceleration for each block
jerk = [50, 29, 50] #allowable jerk
tsample = Decimal(0.01) #Interpolation period
#tolerance
linearErr = Decimal(0.001)
#corner parameters

velocity_list = []

for i in range (1,2):
    #расчет длины пути
    blocklen = Decimal(Interpolation.LengthLinear(trajectory[i], trajectory[i+1])).quantize(Decimal("1.0000"))
    print("Блок " + str(i+1) + ". Длина пути: " + str(blocklen) + " мм.")

    #предварительный расчет длины разгона и торможения
    Nm = floor(acceleration[i]/(jerk[i]*tsample))
    Velstart = 4 #начальная скорость на сегменте
    Velfinish = 5 #конечная скорость на сегменте
    
    LengthAcc = AccDecControl.AccDecDisplacement (Velstart, feedrate[i], jerk[i], acceleration[i], tsample, Nm) #длина разгона
    LengthDec = AccDecControl.AccDecDisplacement (feedrate[i], Velfinish, jerk[i], acceleration[i], tsample, Nm) #длина торможения
    print("Предварительная длина разгона: " + str(LengthAcc) + " мм.")
    print("Предварительная длина торможения: " + str(LengthDec) + " мм.")

    #расчет реальной максимальной скорости
    MaxFeedrate = AccDecControl.RealMaxFeedrate (Velstart, Velfinish, feedrate[i], blocklen, Nm, LengthAcc, LengthDec, linearErr, jerk[i], acceleration[i], tsample)
    print("Максимальная скорость сегмента: " + str(MaxFeedrate[0]) + " мм/c.")
    print("Длина разгона и торможения: " + str(MaxFeedrate[1]) + " мм.")
    
    #построение профиля скорости
    Profile = AccDecControl.AccDecType (Velstart, Velfinish, MaxFeedrate[0], blocklen, jerk[i], acceleration[i], tsample, Nm)
    velocity_list += Profile[0]+Profile[1]+Profile[2]

"""
#вывод графического материала
timelist = []
time = 0
for i in range (len(velocity_list)):
    time += tsample
    timelist.append(time)
Graphs.Graph_01 (timelist, velocity_list,
                 'Время, с', 'Скорость, мм/с', 'Профиль скорости', 'Скорость инструмента') #вывод графика профиля скорости
"""
