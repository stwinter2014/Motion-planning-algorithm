from math import floor
import Interpolation
import AccDecControl
import Graphs

#input data
move_type = [0]    #type of trajectory for each block (0 - linear, 1 - circular, 2 - curve)
trajectory = [[0,0], [100, 100], [100, 90], [100, 0]]   #trajectory points
feedrate = [30, 25, 30]     #list of feedrates for each block
feedrate_max = [30, 30, 30]
acceleration = [25, 25] #allowable acceleration for each block
deceleration = [25, 25] #allowable deceleration for each block
jerk = [10, 10]
tsample = 0.01
#tolerance
linearErr = 0.01
#corner parameters


#расчет длины пути
blocklen = Interpolation.LengthLinear(trajectory[1], trajectory[2])
print("Длина пути: " + str(blocklen) + " мм.")

#предварительный расчет длины разгона и торможения
Nm = floor(acceleration[0]/(jerk[0]*tsample))

for i in range (0, 30):
    LengthAcc = AccDecControl.AccDecDisplacement (0, i, jerk[0], acceleration[0], tsample, Nm)
    #LengthDec = AccDecControl.AccDecDisplacement (feedrate[0], 0, jerk[0], acceleration[0], tsample, Nm)
    print("Предварительная длина разгона: " + str(LengthAcc[0]) + " мм.")
    print("Предварительная длина торможения: " + str(LengthAcc[2]) + " мм.")
    print("Ошибка: " + str(LengthAcc[0]-LengthAcc[2]))
    print("______________________________________________________")

