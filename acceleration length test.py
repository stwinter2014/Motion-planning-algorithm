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
jerk = [50, 10]
tsample = 0.01
#tolerance
linearErr = 0.01
#corner parameters



#расчет длины пути
blocklen = Interpolation.LengthLinear(trajectory[0], trajectory[1])

#предварительный расчет длины разгона и торможения
Nm = floor(acceleration[0]/(jerk[0]*tsample))

length_list = []
length_list1 = []
feedlist = []
i = 5
while i <= feedrate[1]:
    LengthAcc = AccDecControl.AccDecDisplacement (3, i, jerk[0], acceleration[0], tsample, Nm)
    #LengthDec = AccDecControl.AccDecDisplacement (feedrate[1], 0, jerk[0], acceleration[0], tsample, Nm)
    #print("Предварительная длина разгона: " + str(LengthAcc[2]) + " мм.")
    #print("Предварительная длина торможения: " + str(LengthDec[2]) + " мм.")
    length_list.append(LengthAcc) #быстрый расчет
    feedlist.append(i)
    i += 0.1

#вывод графического материала
Graphs.Graph_01 (feedlist, length_list,
                 'Время, с', 'Длина пути, мм', 'Длина разгона при разных скоростях от 0 до 25 мм/с', 'Длина разгона')

for i in range (0, len(length_list)):
    if i > 0:
        a = length_list[i] - length_list[i-1]
        if a >= 0:
            #print('фух')
            pass
        else:
            print('неееееееееееееет')

