from math import floor
from decimal import Decimal
import Interpolation
import AccDecControl
import Graphs

#input data
move_type = [0]    #type of trajectory for each block (0 - linear, 1 - circular, 2 - curve)
trajectory = [[0,0], [100, 100], [100, 90], [15, 10], [16, 13], [16, 18]]   #trajectory points
feedrate = [50, 25, 100, 100, 100]     #list of feedrates for each block
feedrate_max = [60, 75, 60, 50, 60]
acceleration = [500, 500, 5000, 5000, 5000] #allowable acceleration for each block
deceleration = [5000, 5000, 5000, 5000, 5000] #allowable deceleration for each block
jerk = [5000, 5000, 50000, 50000, 50000]
#период интерполяции
tsample = Decimal(0.01).quantize(Decimal("1.0000"))
#tolerance
linearErr = Decimal(0.01).quantize(Decimal("1.0000"))
radiusErr = Decimal(0.005).quantize(Decimal("1.0000"))
#corner parameters



#расчет длины пути
blocklen = Decimal(Interpolation.LengthLinear(trajectory[0], trajectory[1])).quantize(Decimal("1.0000"))

#предварительный расчет длины разгона и торможения
Nm = floor(acceleration[0]/(jerk[0]*tsample))

length_list = []
length_list1 = []
feedlist = []
i = Decimal(6).quantize(Decimal("1.0000"))

while i <= feedrate[1]:
    LengthAcc = AccDecControl.AccDecDisplacement (3, i, jerk[0], acceleration[0], tsample, Nm)
    LengthDec = AccDecControl.AccDecDisplacement (i, 3, jerk[0], acceleration[0], tsample, Nm)
    #print("Предварительная длина разгона: " + str(LengthAcc[2]) + " мм.")
    #print("Предварительная длина торможения: " + str(LengthDec[2]) + " мм.")
    length_list.append(LengthAcc+LengthDec) #быстрый расчет
    #print(length_list[-1])
    feedlist.append(i)
    i += Decimal(0.01).quantize(Decimal("1.0000"))
    #print(i)

#вывод графического материала
Graphs.Graph_01 (feedlist, length_list,
                 'Время, с', 'Длина пути, мм', 'Длина разгона при разных скоростях от 0 до 25 мм/с', 'Длина разгона')
print(len(length_list))
for i in range (0, len(length_list)):
    if i > 0:
        a = length_list[i] - length_list[i-1]
        if a >= 0:
            #print('фух')
            pass
        else:
            print('неееееееееееееет')

