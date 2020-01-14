#LookAhead алгоритм
#определяет начальную и конечную скорость блока.

#скорость на углу
def CornerFeedrate (acc, tsam, angle):
    cornerfeed = acc*tsam/(1-cos(angle))
    corneracc = 30-30*cos(angle)/tsam
    return cornerfeed, corneracc


#AccDec control
#Определение типа блока - короткий или нормальный. Вызывает соответствующие функции.
def DetermineVelProfile (acc, dec, feed, vellast, velnext, length, tsam, tlast):
    times = []
    if vellast < feed:
        lengthAcc = (feed-vellast)**2/acc
    elif vellast >= feed:
        lengthAcc = 0
    if velnext < feed:
        lengthDec = (feed-velnext)**2/dec
    elif velnext >= feed:
        lengthDec = 0
    lengthAccDec = lengthAcc + lengthDec
    if length < lengthAccDec:
        AccDecSmallBlock ()
    else:
        times = AccDecNormalBlock (acc, dec, feed, vellast, velnext, length, lengthAccDec, tsam, tlast)
    return times

def AccDecSmallBlock (acc, dec, feed, vellast, velnext, length, lengthaccdec, tsam, tlast):
    print("block is small")
    velList = []
    timeList = []
    timeinstant = 0
    if vellast >= feed:
        tacc = 0
    if velnext >= feed:
        tdec = 0

#Профиль скорости для нормального блока
"""Входные данные:
1. максимальное ускорение, мм/с2;
2. максимальное торможение, мм/с2;
3. подача, мм/с;
4. подача на предыдущем блоке, мм/с;
5. подача на следующем блоке, мм/с;
6. длина пути на блоке, мм;
7. длина пути при разгоне и торможении, мм;
8. время интерполяции, с;
9. время окончания обработки предыдущего блока, с.
Выходные данные:
1. список скоростей для каждого времени интерполяции, мм/с;
2. список временных точек, с;
3. конечная скорость, мм/с;
4. конечное время, с."""
def AccDecNormalBlock (acc, dec, feed, vellast, velnext, length, lengthaccdec, tsam, tlast):
    velList = []
    timeList = []
    timeinstant = 0
    print("Тип блока нормальный")
    #расчет времени разгона/торможения и построянной скорости
    if vellast >= feed:
        tacc = 0
    else:
        tacc = 2*(feed-vellast)/acc
    if velnext >= feed:
        tdec = 0
    else:
        tdec = 2*(feed-velnext)/dec
    if lengthaccdec == length:
        tconst = 0
    else:
        tconst = (length - lengthaccdec)/feed
    #расчет профиля скорости
    while timeinstant <= tacc and tacc != 0:
        velAcc = vellast + acc/2*(tacc/(2*pi))*((2*pi)/tacc*timeinstant-sin((2*pi)/tacc*timeinstant))
        velList.append(velAcc)
        timeList.append(timeinstant)
        timeinstant += tsam
    while timeinstant <= tacc + tconst:
        velConst = feed
        velList.append(velConst)
        timeList.append(timeinstant)
        timeinstant += tsam
    while timeinstant <= tacc + tconst + tdec:
        timed = tacc + tconst
        velDec = dec/2*(-(timeinstant - timed)-(tdec/(2*pi))*sin((2*pi)/tdec*(-(timeinstant - timed)))) + velConst
        velList.append(velDec)
        timeList.append(timeinstant)
        timeinstant += tsam
    #корректировка времени
    for i in range (len(timeList)):
        timeList[i] = timeList[i] + tlast
    #сохранение последней скорости для следующего блока
    if tdec == 0:
        velfinish = velConst
    else:
        velfinish = velList[-1]
    #сохранение последнего времени для следующего блока
    tfinish = timeList[-1]
    return velList, timeList, velfinish, tfinish
