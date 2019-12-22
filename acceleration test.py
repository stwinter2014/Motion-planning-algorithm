from math import floor
import Interpolation
import AccDecControl
import Graphs

#input data
move_type = [0]    #type of trajectory for each block (0 - linear, 1 - circular, 2 - curve)
trajectory = [[0,0], [100, 100], [100, 90], [100, 0]]   #trajectory points
feedrate = [30, 15, 30]     #list of feedrates for each block
feedrate_max = [30, 30, 30]
acceleration = [25, 25] #allowable acceleration for each block
deceleration = [25, 25] #allowable deceleration for each block
jerk = [50, 10]
tsample = 0.01
#tolerance
linearErr = 0.01
#corner parameters

#расчет длины пути
blocklen = Interpolation.LengthLinear(trajectory[0], trajectory[1])
print("Длина пути: " + str(blocklen) + " мм.")

#предварительный расчет длины разгона и торможения
Nm = floor(acceleration[0]/(jerk[0]*tsample))

LengthAcc = AccDecControl.AccDecDisplacement (3, feedrate[1], jerk[0], acceleration[0], tsample, Nm)
#LengthDec = AccDecControl.AccDecDisplacement (feedrate[1], 0, jerk[0], acceleration[0], tsample, Nm)
print("Предварительная длина разгона: " + str(LengthAcc) + " мм.")
#print("кол-во шагов на разгоне " + str(LengthAcc[4][0]))
#print("кол-во шагов на постоянн " + str(LengthAcc[4][1]))
#print("кол-во шагов на торможе " + str(LengthAcc[4][2]))
Profile = AccDecControl.AccVelProfiles (3, feedrate[1], jerk[0], acceleration[0], tsample, Nm)
#вывод графического материала
timelist = []
time = 0
for i in range (len(Profile[1])):
    time += tsample
    timelist.append(time)
Graphs.Graph_01 (timelist, Profile[1],
                 'Время, с', 'Скорость, мм/с', 'Профиль скорости', 'Скорость инструмента')
