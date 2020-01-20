from math import floor
from decimal import Decimal
import Interpolation
import AccDecControl
import Graphs

#input data
move_type = [0]    #type of trajectory for each block (0 - linear, 1 - circular, 2 - curve)
trajectory = [[0,0], [10, 10], [10, 9], [13, 10], [14, 13], [16, 15]]   #trajectory points
feedrate = [50, 80, 60, 50, 45]     #list of feedrates for each block
feedrate_max = [100, 100, 100, 100, 100]
acceleration = [500, 500, 500, 500, 500] #allowable acceleration for each block
deceleration = [5000, 5000, 5000, 5000, 5000] #allowable deceleration for each block
jerk = [5000, 5000, 5000, 5000, 5000]
#период интерполяции
tsample = Decimal(0.004).quantize(Decimal("1.0000"))
#tolerance
linearErr = Decimal(0.01).quantize(Decimal("1.0000"))
radiusErr = Decimal(0.005).quantize(Decimal("1.0000"))
#corner parameters

velocity_list = []

for i in range (0,2):
    #расчет длины пути
    blocklen = Decimal(Interpolation.LengthLinear(trajectory[i], trajectory[i+1])).quantize(Decimal("1.0000"))
    print("Участок " + str(i+1) + ". Длина пути: " + str(blocklen) + " мм.")
    #print("Участок " + str(i+1) + ".")
    #предварительный расчет длины разгона и торможения
    Nm = floor(acceleration[i]/(jerk[i]*tsample))

    LengthAcc = AccDecControl.AccDecDisplacement (0, feedrate[i], jerk[i], acceleration[i], tsample, Nm)
    LengthDec = AccDecControl.AccDecDisplacement (feedrate[i], 0, jerk[i], acceleration[i], tsample, Nm)
    print("     Длина разгона: " + str(LengthAcc) + " мм.")
    print("     Длина торможения: " + str(LengthDec) + " мм.")
"""
    #расчет реальной максимальной скорости
    MaxFeedrate = AccDecControl.RealMaxFeedrate (0, 0, feedrate[i], blocklen, Nm, LengthAcc, LengthDec, linearErr, jerk[i], acceleration[i], tsample)
    print("Макс. скорость: " + str(MaxFeedrate[0]) + " мм/c.")
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
"""
"""
Vs= 0
Ve = 0
blocklen_list = []
blocklen_list.append(Decimal(Interpolation.LengthLinear(trajectory[0], trajectory[1])).quantize(Decimal("1.0000")))
blocklen_list.append(Decimal(Interpolation.LengthLinear(trajectory[1], trajectory[2])).quantize(Decimal("1.0000")))
blocklen_list.append(Decimal(Interpolation.LengthLinear(trajectory[2], trajectory[3])).quantize(Decimal("1.0000")))
blocklen_list.append(Decimal(Interpolation.LengthLinear(trajectory[3], trajectory[4])).quantize(Decimal("1.0000")))
blocklen_list.append(Decimal(Interpolation.LengthLinear(trajectory[4], trajectory[5])).quantize(Decimal("1.0000")))
Nt = 3
for i in range (0,5):
    print("Участок " + str(i+1) + ". Длина пути: " + str(blocklen_list[i]) + " мм.")
    Nm = floor(acceleration[i]/(jerk[i]*tsample))
    if i == 0:
        Nt = 3
        Vend_i = AccDecControl.LinkedFeedrate (Ve, blocklen_list[0:3], feedrate[0:3], Nm, feedrate_max[0:3], Nt, jerk[0], acceleration[0], tsample, linearErr)
        Ve = Vend_i
        print("Конечная скорость участка: " + str(Ve) + " мм/с.")
    if i == 1:
        Vs = Ve
        Nt = 3
        Vend_i = AccDecControl.LinkedFeedrate (Ve, blocklen_list[1:4], feedrate[1:4], Nm, feedrate_max[1:4], Nt, jerk[0], acceleration[0], tsample, linearErr)
        Ve = Vend_i
        print("Конечная скорость участка: " + str(Ve) + " мм/с.")
    if i == 2:
        Vs = Ve
        Nt = 3
        Vend_i = AccDecControl.LinkedFeedrate (Ve, blocklen_list[2:5], feedrate[2:5], Nm, feedrate_max[2:5], Nt, jerk[0], acceleration[0], tsample, linearErr)
        Ve = Vend_i
        print("Конечная скорость участка: " + str(Ve) + " мм/с.")
    if i == 3:
        Vs = Ve
        Nt = 2
        Vend_i = AccDecControl.LinkedFeedrate (Ve, blocklen_list[3:5], feedrate[3:5], Nm, feedrate_max[3:5], Nt, jerk[0], acceleration[0], tsample, linearErr)
        Ve = Vend_i
        print("Конечная скорость участка: " + str(Ve) + " мм/с.")
    if i == 4:
        Vs = Ve
        Nt = 1
        Vend_i = AccDecControl.LinkedFeedrate (Ve, blocklen_list[4], feedrate[4], Nm, feedrate_max[4], Nt, jerk[0], acceleration[0], tsample, linearErr)
        Ve = Vend_i
        print("Конечная скорость участка: " + str(Ve) + " мм/с.")

    blocklen = Decimal(Interpolation.LengthLinear(trajectory[i], trajectory[i+1])).quantize(Decimal("1.0000"))
    #предварительный расчет длины разгона и торможения
    Nm = floor(acceleration[i]/(jerk[i]*tsample))
    
    LengthAcc = AccDecControl.AccDecDisplacement (Vs, feedrate[i], jerk[i], acceleration[i], tsample, Nm)
    LengthDec = AccDecControl.AccDecDisplacement (feedrate[i], Ve, jerk[i], acceleration[i], tsample, Nm)
    print("Предварительная длина разгона: " + str(LengthAcc) + " мм.")
    print("Предварительная длина торможения: " + str(LengthDec) + " мм.")

    #расчет реальной максимальной скорости
    MaxFeedrate = AccDecControl.RealMaxFeedrate (Vs, Ve, feedrate[i], blocklen, Nm, LengthAcc, LengthDec, linearErr, jerk[i], acceleration[i], tsample)
    #print("Максимальная скорость сегмента: " + str(MaxFeedrate[0]) + " мм/c.")
    #print("Длина разгона и торможения: " + str(MaxFeedrate[1]) + " мм.")

    #построение профиля скорости
    Profile = AccDecControl.AccDecType (Vs, Ve, MaxFeedrate[0], blocklen, jerk[i], acceleration[i], tsample, Nm)
    velocity_list += Profile[0]+Profile[1]+Profile[2]
    print("_______________________________________________")
#вывод графического материала
timelist = []
time = 0
for i in range (len(velocity_list)):
    time += tsample
    timelist.append(time)
Graphs.Graph_01 (timelist, velocity_list,
                 'Время, с', 'Скорость, мм/с', 'Профиль скорости', 'Скорость инструмента')
"""
"""
#пример расчета реальной конечной скорости с учетом длины пути
Nm = floor(acceleration[0]/(jerk[0]*tsample))
blocklen = Decimal(Interpolation.LengthLinear(trajectory[0], trajectory[1])).quantize(Decimal("1.0000"))
Ve = AccDecControl.EndingVel (blocklen, 0, feedrate[0], jerk[0], acceleration[0], tsample, Nm, linearErr)
print("Максимально достижимая скорость на участке 1: " + str(Ve) + " мм/с")
Nm = floor(acceleration[1]/(jerk[1]*tsample))
blocklen = Decimal(Interpolation.LengthLinear(trajectory[1], trajectory[2])).quantize(Decimal("1.0000"))
Ve = AccDecControl.EndingVel (blocklen, 0, feedrate[1], jerk[1], acceleration[1], tsample, Nm, linearErr)
print("Максимально достижимая скорость на участке 1: " + str(Ve) + " мм/с")
LengthAcc = AccDecControl.AccDecDisplacement (0, Ve, jerk[1], acceleration[1], tsample, Nm)
print("Предварительная длина разгона: " + str(LengthAcc) + " мм.")
"""
