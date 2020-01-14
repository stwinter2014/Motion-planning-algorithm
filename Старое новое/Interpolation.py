from math import fabs, sqrt, pow

"""Подсчет длины траектории при линейной траектории.
Входные данные:
1. Координаты начальной точки [x, y, z];
2. координаты конечной точки [x, y, z].
Выходные данные:
1. Длина траектории, мм."""
def LengthLinear(start, end):
    length = sqrt((pow((end[0]-start[0]), 2))+(pow((end[1]-start[1]), 2)))
    return length


#Линейная интерполяция
"""Расчет движения инструмента по координатам.
Входные данные:
1. координаты начальной точки [x, y];
2. координаты конечной точки [x, y];
3. список скоростей, мм/с;
4. скорость на предыдущем блоке, мм/с;
5. длина блока, мм;
6. время интерполяции, с.
Выходные данные:
1. список координат по оси X, мм;
2. список координат по оси Y, мм."""
def InterpolationLinear(p_start, p_finish, vellist, vellast, length, tsam):
    S = 0
    x_list = []
    y_list = []
    x_list.append(p_start[0])
    y_list.append(p_start[1])
    x_tmp = p_start[0]
    y_tmp = p_start[1]
    for i in range (len(vellist)):
        #расчет единичного перемещения
        if i == 0:
            Si = tsam*(vellist[i]+vellast)/2
        else:
            Si = tsam*(vellist[i]+vellist[i-1])/2
        #расчет приращений для каждой координаты
        delta_x = Si*(fabs(p_finish[0]-p_start[0])/length)
        delta_y = Si*(fabs(p_finish[1]-p_start[1])/length)
        x_tmp += delta_x
        y_tmp += delta_y
        x_list.append(x_tmp)
        y_list.append(y_tmp)
        S += Si
    print("Длина пути по интерполятору: " + str(S))
    return x_list, y_list, S
