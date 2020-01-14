from decimal import Decimal

#n1 = Decimal(4.2)
n1 = Decimal(4.2).quantize(Decimal("1.0000"))
n2 = Decimal(4)
n2 = n2.quantize(Decimal("1.0000"))

n3 = n1*n2
print(n3)
print(type(n3))
