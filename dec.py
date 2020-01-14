from decimal import Decimal
from math import fabs

V1 = Decimal(5)
V1 = V1.quantize(Decimal("1.0000"))
V2 = Decimal(15)
V2 = V2.quantize(Decimal("1.0000"))
V3 = Decimal(0.5)*(V1+V2)
V3 = V3.quantize(Decimal("1.0000"))

print(V3)
