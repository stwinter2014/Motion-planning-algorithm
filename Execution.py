from math import floor
import Interpolation
import AccDecControl
import Graphs

#input data
move_type = [0]    #type of trajectory for each block (0 - linear, 1 - circular, 2 - curve)
trajectory = [[0,0], [100, 100], [100, 90], [100, 0]]   #trajectory points
feedrate = [30, 25, 30]     #list of feedrates for each block
#feedrate_max = [30, 30, 30]
acceleration = [25, 25, 25] #allowable acceleration for each block
deceleration = [25, 25, 25] #allowable deceleration for each block
jerk = [50, 50, 50]
tsample = 0.01
#tolerance
linearErr = 0.01
#corner parameters

velocity_list = []
for i in range (0,2):
    #расчет длины пути
    blocklen = Interpolation.LengthLinear(trajectory[i], trajectory[i+1])
    print("Блок " + str(i) + ". Длина пути: " + str(blocklen) + " мм.")

    #предварительный расчет длины разгона и торможения
    Nm = floor(acceleration[i]/(jerk[i]*tsample))

    LengthAcc = AccDecControl.AccDecDisplacement (0, feedrate[i], jerk[i], acceleration[i], tsample, Nm)
    LengthDec = AccDecControl.AccDecDisplacement (feedrate[i], 0, jerk[i], acceleration[i], tsample, Nm)
    print("Предварительная длина разгона: " + str(LengthAcc) + " мм.")
    print("Предварительная длина торможения: " + str(LengthDec) + " мм.")

    #расчет реальной максимальной скорости
    MaxFeedrate = AccDecControl.RealMaxFeedrate (0, 0, feedrate[i], blocklen, Nm, LengthAcc, LengthDec, linearErr, jerk[i], acceleration[i], tsample)
    print("Максимальная скорость сегмента: " + str(MaxFeedrate[0]) + " мм/c.")
    print("Длина разгона и торможения: " + str(MaxFeedrate[1]) + " мм.")

    #построение профиля скорости
    Profile = AccDecControl.AccDecType (0, 0, MaxFeedrate[0], blocklen, jerk[i], acceleration[i], tsample, Nm)
    velocity_list += Profile[0]+Profile[1]+Profile[2]

#вывод графического материала
timelist = []
time = 0
for i in range (len(velocity_list)):
    time += tsample
    timelist.append(time)
Graphs.Graph_01 (timelist, velocity_list,
                 'Время, с', 'Скорость, мм/с', 'Профиль скорости', 'Скорость инструмента')

"""
N = 3
blocklen_list = []
Vlast = 0
for i in range (len(feedrate)):
    blocklen_list.append(Interpolation.LengthLinear(trajectory[i], trajectory[i+1]))
for i in range (len(feedrate)):
    if len(feedrate[i:N]) < N:
        N -=1
        print('da')
    print("Длина пути: " + str(blocklen_list[i]) + " мм.")
    Vend_i = AccDecControl.LinkedFeedrate (Vlast, blocklen_list[i:N], feedrate[i:N], Nm, feedrate_max[i:N], N, jerk[0], acceleration[0], tsample, linearErr)
    Vlast = Vend_i
    print(Vend_i)
"""
"""
#print(AccDecControl.EndingVel (blocklen, 20, 25, jerk[0], acceleration[0], tsample, Nm, linearErr))
LengthAcc = AccDecControl.AccDecDisplacement (20, 25, jerk[0], acceleration[0], tsample, Nm)
LengthDec = AccDecControl.AccDecDisplacement (25, 25, jerk[0], acceleration[0], tsample, Nm)
print(AccDecControl.RealMaxFeedrate (20, 25, 25, blocklen, Nm, LengthAcc[0], LengthDec[0], linearErr, jerk[0], acceleration[0], tsample))
"""
