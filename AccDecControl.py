from math import pi, cos, sin, fabs, sqrt, ceil, floor

#LOOK AHEAD ALGORITHM
def LinkedFeedrate (Vend_last, l_list, feed_list, Nm, Vemax_list, N, j_max, acc_max, Tint, maxErr):
    print(l_list)
    print(feed_list)
    print(Vemax_list)
    if N == 0:
        Vend = 0
    else:
        Ve0 = EndingVel(l_list[0], Vend_last, feed_list[0], j_max, acc_max, Tint, Nm, maxErr)
        print("Ve0 " + str(Ve0))
        K = N - 1
        Ve1 = 0
        while K >= 1:
            Ve1 = EndingVel(l_list[K], Ve1, feed_list[K], j_max, acc_max, Tint, Nm, maxErr)
            Ve1 = min(Ve1, Vemax_list[K])
            print("Ve1 " + str(Ve1))
            K -= 1
            print(K)
        Vend = min(Ve0, Ve1)
    return Vend

#actual ending velocity
def EndingVel (length, Vstart, Vobj, j_max, acc_max, Tint, Nm, maxErr):
    if Vstart == Vobj or length >= AccDecDisplacement (Vstart, Vobj, j_max, acc_max, Tint, Nm):
        Ve = Vobj
    else:
        print('priv')
        vl_k = min(Vstart, Vobj)
        vh_k = max(Vstart, Vobj)
        ve_k = 1/2*(vl_k + vh_k)
        S_k = AccDecDisplacement (Vstart, ve_k, j_max, acc_max, Tint, Nm)
        print(S_k)
        while fabs(S_k - length) > maxErr:
            if (Vstart - Vobj)*(S_k - length) > 0:
                vl_k = ve_k
            else:
                vh_k = ve_k
            ve_k = 1/2*(vl_k + vh_k)
            S_k = AccDecDisplacement (Vstart, ve_k, j_max, acc_max, Tint, Nm)
            print(S_k)
            print('vl_k ', str(vl_k))
            print('vh_k ', str(vh_k))
            print("________________")
        Ve = ve_k
    return Ve

#предварительный расчет длины разгона или торможения инструмента
def AccDecDisplacement (V1, V2, j_max, acc_max, Tint, Nm):
    acclist = []
    vellist = []
    check_1 = 0
    check_2 = 0
    check_3 = 0
    if V1 == V2: #разгон/торможение не требуются
        vellist = []
        LAccDec = 0
    else:
        J = 0
        n1 = 0
        n2 = 0
        M1 = (fabs(V1 - V2))/(Nm*j_max*(Tint**2)) - Nm
        M2 = sqrt(fabs(V1 - V2)/(j_max*(Tint**2)))
        if M1 > 0:
            n1 = Nm
            n2 = ceil(M1) #ceiling
        elif M1 <= 0:
            n1 = ceil(M2) #ceiling
            n2 = 0
        A2 = 1/((2*n1+n2-1)*Tint)*(fabs(V1 - V2)-(n1 - 1)*(n1 + n2 - 1)*j_max*(Tint**2))
        if V1 < V2:
            a2 = A2
            J = j_max
        elif V1 > V2:
            a2 = -A2
            J = - j_max
        a = (2*n1+n2)*V1*Tint
        b = 1/2*a2*(4*(n1**2)+4*n1*n2+n2**2-2*n1-n2)*(Tint**2)
        c = 1/2*(2*n1**3+3*(n1**2)*n2+n1*(n2**2)-4*n1**2-4*n1*n2-n2**2+2*n1+n2)*J*(Tint**3)
        LAccDec = a + b + c
    return LAccDec

#истинная максимальная скорость
def RealMaxFeedrate (Vstart, Vend, feedrate, length, Nm, LAcc, LDec, maxErr, j_max, acc_max, Tint):
    if LAcc + LDec < length:
        print("Сегмент содержит участок с постоянной скоростью.")
        maxfeed = feedrate
        s = LAcc + LDec
    else:
        k = 0
        vl = max(Vstart, Vend)
        vh = feedrate
        print('vl = ' + str(vl))
        print('vh = ' + str(vh))
        vm_k = 1/2*(vl + vh)
        print('vm_k = ' + str(vm_k))
        sm_k = AccDecDisplacement(Vstart, vm_k, j_max, acc_max, Tint, Nm) + AccDecDisplacement(vm_k, Vend, j_max, acc_max, Tint, Nm)
        print('sm_k = ' + str(sm_k))
        while fabs(sm_k - length) > maxErr:
            print('погрешность = ' + str(sm_k - length))
            print('____________________________________________________________')
            k += 1
            if sm_k < length:
                vl = vm_k
                print('vl = ' + str(vl))
                print('vh = ' + str(vh))
            else:
                vh = vm_k
                print('vl = ' + str(vl))
                print('vh = ' + str(vh))
            vm_k = 1/2*(vl + vh)
            print('vm_k = ' + str(vm_k))
            sm_k = AccDecDisplacement(Vstart, vm_k, j_max, acc_max, Tint, Nm) + AccDecDisplacement(vm_k, Vend, j_max, acc_max, Tint, Nm)
            print('sm_k = ' + str(sm_k))
        maxfeed = vm_k
        s = sm_k
    return maxfeed, s


def AccDecType (Vstart, Vend, Vmax, length, j_max, acc_max, Tint, Nm):
    const = []
    Lconst = 0
    if Vstart < Vmax:
        Lacc = AccDecDisplacement(Vstart, Vmax, j_max, acc_max, Tint, Nm)
        acc = AccVelProfiles(Vstart, Vmax, j_max, acc_max, Tint, Nm)[0]
    else:
        Lacc = 0
    if Vend < Vmax:
        Ldec = AccDecDisplacement(Vmax, Vend, j_max, acc_max, Tint, Nm)
        dec = AccVelProfiles(Vmax, Vend, j_max, acc_max, Tint, Nm)[0]
    else:
        Ldec = 0
    l = Lconst + Lacc + Ldec
    while l < length:
        if fabs(l-length) < Lconst/2:
            break
        else:
            const.append(Vmax)
            Lconst = Tint*Vmax
            l = l + Lconst
    return acc, const, dec

#генерация профиля скорости на участках разгона/торможения
def AccVelProfiles (V1, V2, j_max, acc_max, Tint, Nm):
    acclist = []
    vellist = []
    check_1 = 0
    check_2 = 0
    check_3 = 0
    if V1 == V2: #разгон/торможение не требуются
        vellist = []
    else:
        J = 0
        n1 = 0
        n2 = 0
        M1 = (fabs(V1 - V2))/(Nm*j_max*(Tint**2)) - Nm
        M2 = sqrt(fabs(V1 - V2)/(j_max*(Tint**2)))
        if M1 > 0:
            n1 = Nm
            n2 = ceil(M1) #ceiling
        elif M1 <= 0:
            n1 = ceil(M2) #ceiling
            n2 = 0
        A2 = 1/((2*n1+n2-1)*Tint)*(fabs(V1 - V2)-(n1 - 1)*(n1 + n2 - 1)*j_max*(Tint**2))
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
                ai = a2 + (i - 2)*J*Tint
                vi = vellist[-1] + ai*Tint
                acclist.append(ai)
                vellist.append(vi)
                check_1 += 1
            elif i > n1 + 1 and i <= n1 + n2 + 1:
                ai = a2 + (n1 - 1)*J*Tint
                vi = vellist[-1] + ai*Tint
                acclist.append(ai)
                vellist.append(vi)
                check_2 += 1
            elif i > n1 + n2 + 1 and i <= 2*n1 + n2:
                ai = a2 + (2*n1 + n2 - i)*J*Tint
                vi = vellist[-1] + ai*Tint
                acclist.append(ai)
                vellist.append(vi)
                check_3 += 1
    return vellist, acclist, [check_1, check_2, check_3]
