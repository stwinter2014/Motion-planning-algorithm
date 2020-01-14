from math import pi, cos, sin, fabs, sqrt, ceil, floor
from decimal import Decimal

#LOOK AHEAD ALGORITHM
def LinkedFeedrate (Vend_last, l_list, feed_list, Nm, Vemax_list, N, j_max, acc_max, Tint, maxErr):
    #print(l_list)
    #print(feed_list)
    #print(Vemax_list)
    if N == 0:
        Vend = 0
    else:
        Ve0 = EndingVel(l_list[0], Vend_last, feed_list[0], j_max, acc_max, Tint, Nm, maxErr)
        print("Ve0 " + str(Ve0))
        K = N - 1
        Ve1 = 0
        while K >= 1:
            if feed_list[K] == 80:
                print("Ve1 вот вот вот " + str(Ve1))
            Ve1 = EndingVel(l_list[K], Ve1, feed_list[K], j_max, acc_max, Tint, Nm, maxErr)
            print("Ve1 " + str(Ve1))
            Ve1 = min(Ve1, Vemax_list[K])
            #print("Ve1 " + str(Ve1))
            K -= 1
            #print(K)
        Vend = min(Ve0, Ve1)
    return Vend

#actual ending velocity
def EndingVel (length, Vstart, Vobj, j_max, acc_max, Tint, Nm, maxErr):
    if Vstart == Vobj or length >= AccDecDisplacement (Vstart, Vobj, j_max, acc_max, Tint, Nm):
        Ve = Vobj
    else:
        vl_k = min(Vstart, Vobj)
        vh_k = max(Vstart, Vobj)
        ve_k = (Decimal(1/2)*(vl_k + vh_k)).quantize(Decimal("1.0000"))
        S_k = AccDecDisplacement (Vstart, ve_k, j_max, acc_max, Tint, Nm)
        #print(S_k)
        k = 0
        S_klength_fabs = Decimal(fabs(S_k - length)).quantize(Decimal("1.0000"))
        while S_klength_fabs > maxErr and k < 50:
            if (Vstart - Vobj)*(S_k - length) > 0:
                vl_k = ve_k
            else:
                vh_k = ve_k
            ve_k = (Decimal(1/2)*(vl_k + vh_k)).quantize(Decimal("1.0000"))
            S_k = AccDecDisplacement (Vstart, ve_k, j_max, acc_max, Tint, Nm)
            #print(S_k)
            #print('vl_k ', str(vl_k))
            print('ve_k ', str(ve_k))
            #print("________________")
            k += 1
            if k == 49:
                print("Достигнуто максимальное число итераций")
        Ve = ve_k
    return Ve

#предварительный расчет длины разгона или торможения инструмента
def AccDecDisplacement (V1, V2, j_max, acc_max, Tint, Nm):
    acclist = []
    vellist = []
    if V1 == V2: #разгон/торможение не требуются
        vellist = []
        LAccDec = 0
    else:
        J = Decimal(0).quantize(Decimal("1.0000"))
        n1 = int(0)
        n2 = int(0)
        V1V2fabs = Decimal(fabs(V1 - V2)).quantize(Decimal("1.0000"))
        M1 = ((V1V2fabs)/(Nm*j_max*(Tint*Tint)) - Nm).quantize(Decimal("1.0000"))
        M2 = Decimal(sqrt(V1V2fabs/(j_max*(Tint*Tint)))).quantize(Decimal("1.0000"))
        #print(type(M2))
        #print(M2)
        if M1 > 0:
            n1 = Nm
            n2 = ceil(M1) #ceiling
        elif M1 <= 0:
            n1 = ceil(M2) #ceiling
            n2 = 0
        A2 = (1/((2*n1+n2-1)*Tint)*(V1V2fabs -(n1 - 1)*(n1 + n2 - 1)*j_max*(Tint*Tint))).quantize(Decimal("1.0000"))
        #print(A2)
        if V1 < V2:
            a2 = A2
            J = j_max
        elif V1 > V2:
            a2 = -A2
            J = - j_max
        a = ((2*n1+n2)*V1*Tint).quantize(Decimal("1.0000"))
        #print(a)
        b = (Decimal(1/2)*a2*(4*(n1**2)+4*n1*n2+n2**2-2*n1-n2)*(Tint*Tint)).quantize(Decimal("1.0000"))
        #print(b)
        c = (Decimal(1/2)*(2*n1**3+3*(n1**2)*n2+n1*(n2**2)-4*n1**2-4*n1*n2-n2**2+2*n1+n2)*J*(Tint*Tint*Tint)).quantize(Decimal("1.0000"))
        #print(c)
        LAccDec = a + b + c
    return LAccDec

#истинная максимальная скорость
def RealMaxFeedrate (Vstart, Vend, feedrate, length, Nm, LAcc, LDec, maxErr, j_max, acc_max, Tint):
    if LAcc + LDec < length:
        print("Сегмент содержит участок с постоянной скоростью.")
        maxfeed = feedrate
        s = LAcc + LDec
        Vlist = []
        Slist = []
    else:
        k = 0
        vl = max(Vstart, Vend)
        vh = feedrate
        #print('vl = ' + str(vl))
        #print('vh = ' + str(vh))
        vm_k = (Decimal(1/2)*(vl + vh)).quantize(Decimal("1.0000"))
        #print('vm_k = ' + str(vm_k))
        #print(type(vm_k))
        sm_k = AccDecDisplacement(Vstart, vm_k, j_max, acc_max, Tint, Nm) + AccDecDisplacement(vm_k, Vend, j_max, acc_max, Tint, Nm)
        #print('sm_k = ' + str(sm_k))
        Vlist = []
        Vlist.append(vm_k)
        Slist = []
        Slist.append(sm_k)
        sm_klength_fabs = Decimal(fabs(sm_k - length)).quantize(Decimal("1.0000"))
        while sm_klength_fabs > maxErr and k < 50:
            #print('погрешность = ' + str(sm_k - length))
            #print('____________________________________________________________')
            if sm_k < length:
                vl = vm_k
                #print('vl = ' + str(vl))
                #print('vh = ' + str(vh))
            else:
                vh = vm_k
                #print('vl = ' + str(vl))
                #print('vh = ' + str(vh))
            vm_k = (Decimal(1/2)*(vl + vh)).quantize(Decimal("1.0000"))
            #print('vm_k = ' + str(vm_k))
            sm_k = AccDecDisplacement(Vstart, vm_k, j_max, acc_max, Tint, Nm) + AccDecDisplacement(vm_k, Vend, j_max, acc_max, Tint, Nm)
            #print('sm_k = ' + str(sm_k))
            Vlist.append(vm_k)
            Slist.append(sm_k)
            sm_klength_fabs = Decimal(fabs(sm_k - length)).quantize(Decimal("1.0000"))
            k += 1
            if k == 49:
                print("Достигнуто максимальное число итераций")
        maxfeed = vm_k
        s = sm_k
    return maxfeed, s, Vlist, Slist


def AccDecType (Vstart, Vend, Vmax, length, j_max, acc_max, Tint, Nm):
    const = []
    Lconst = 0
    if Vstart < Vmax:
        Lacc = AccDecDisplacement(Vstart, Vmax, j_max, acc_max, Tint, Nm)
        acc = AccVelProfiles(Vstart, Vmax, j_max, acc_max, Tint, Nm)[0]
    else:
        Lacc = 0
        acc = []
    if Vend < Vmax:
        Ldec = AccDecDisplacement(Vmax, Vend, j_max, acc_max, Tint, Nm)
        dec = AccVelProfiles(Vmax, Vend, j_max, acc_max, Tint, Nm)[0]
    else:
        Ldec = 0
        dec = []
    l = Lconst + Lacc + Ldec
    print("Длина разгона/торможения " + str(l))
    while l < length:
        const.append(Vmax)
        Lconst = Tint*Vmax
        l = l + Lconst
    return acc, const, dec

#генерация профиля скорости на участках разгона/торможения
def AccVelProfiles (V1, V2, j_max, acc_max, Tint, Nm):
    acclist = []
    vellist = []
    if V1 == V2: #разгон/торможение не требуются
        vellist = []
        LAccDec = 0
    else:
        J = Decimal(0).quantize(Decimal("1.0000"))
        n1 = int(0)
        n2 = int(0)
        V1V2fabs = Decimal(fabs(V1 - V2)).quantize(Decimal("1.0000"))
        M1 = ((V1V2fabs)/(Nm*j_max*(Tint*Tint)) - Nm).quantize(Decimal("1.0000"))
        M2 = Decimal(sqrt(V1V2fabs/(j_max*(Tint*Tint)))).quantize(Decimal("1.0000"))
        #print(type(M2))
        #print(M2)
        if M1 > 0:
            n1 = Nm
            n2 = ceil(M1) #ceiling
        elif M1 <= 0:
            n1 = ceil(M2) #ceiling
            n2 = 0
        A2 = (1/((2*n1+n2-1)*Tint)*(V1V2fabs -(n1 - 1)*(n1 + n2 - 1)*j_max*(Tint*Tint))).quantize(Decimal("1.0000"))
        #print(A2)
        if V1 < V2:
            a2 = A2
            J = j_max
        elif V1 > V2:
            a2 = -A2
            J = - j_max
        for i in range (1, (2*n1+n2+1)):
            if i == 1:
                ai = 0
                vi = V1
                acclist.append(ai)
                vellist.append(vi)
            elif i > 1 and i <= n1 + 1:
                ai = (a2 + (i - 2)*J*Tint).quantize(Decimal("1.0000"))
                vi = (vellist[-1] + ai*Tint).quantize(Decimal("1.0000"))
                acclist.append(ai)
                vellist.append(vi)
            elif i > n1 + 1 and i <= n1 + n2 + 1:
                ai = (a2 + (n1 - 1)*J*Tint).quantize(Decimal("1.0000"))
                vi = (vellist[-1] + ai*Tint).quantize(Decimal("1.0000"))
                acclist.append(ai)
                vellist.append(vi)
            elif i > n1 + n2 + 1 and i <= 2*n1 + n2:
                ai = (a2 + (2*n1 + n2 - i)*J*Tint).quantize(Decimal("1.0000"))
                vi = (vellist[-1] + ai*Tint).quantize(Decimal("1.0000"))
                acclist.append(ai)
                vellist.append(vi)
    return vellist, acclist
