from math import floor
from decimal import Decimal
import Interpolation
import AccDecControl
import Graphs

#input data
move_type = [0]    #type of trajectory for each block (0 - linear, 1 - circular, 2 - curve)
trajectory = [[0,0], [100, 100], [100, 90], [100, 0]]   #trajectory points
feedrate = [30, 25, 30]     #list of feedrates for each block
feedrate_max = [30, 30, 30]
acceleration = [25, 25, 25] #allowable acceleration for each block
deceleration = [25, 25, 25] #allowable deceleration for each block
jerk = [50, 50, 50]
#период интерполяции
tsample = Decimal(0.01).quantize(Decimal("1.0000"))
#tolerance
linearErr = Decimal(0.01).quantize(Decimal("1.0000"))
radiusErr = Decimal(0.001).quantize(Decimal("1.0000"))
#corner parameters

Vs = 4
Ve = 5

while (V)
