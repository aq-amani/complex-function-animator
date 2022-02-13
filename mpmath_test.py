from mpmath import *

mp.dps = 10
mp.pretty = True

print('First 10 Riemann zeta function zeros with 10 digits of precision')
for i in range(1,10):
    print(zetazero(i))
