from cs50 import get_float
while True:
    change = get_float("Change owned: ")
    if change > 0.000:
        break

cents = change * 100
n = 0
while (25 * n) <= cents:
    n += 1

n -= 1

cents -= 25 * n

a = n

n = 0

while (10 * n) <= cents:
    n += 1

n -= 1
cents -= 10 * n
b = n

n = 0

while (5 * n) <= cents:
    n += 1

n -= 1

cents -= 5 * n

c = n

n = 0

while (1 * n) <= cents:
    n += 1

n -= 1

cents -= 1 * n

d = n

t = a + b + c + d

print(t)