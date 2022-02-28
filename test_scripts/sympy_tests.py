from sympy import *


print(f'1000 digits of Pi:\n {N(pi, 1000)}\n')
print(f'1000 digits of e:\n {N(E, 1000)}\n')
print(f'1000 digits of Golden Ratio(Phi):\n {N(GoldenRatio, 1000)}\n')
print(f'1000 digits of sqrt 2:\n {N(sqrt(2), 1000)}\n')
print(f'100 terms of fibonacci sequence {[fibonacci(n) for n in range(0,100)]}\n')
print(f'Primes between 1 - 1000 {list(primerange(0, 1000))}\n')
print(f'100 primes {[prime(n) for n in range(1,100)]}\n') # Slow
