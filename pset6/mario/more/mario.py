from cs50 import get_int
while True:
    h = get_int("Height: ")
    if h > 0 and h <= 8:
        break

for i in range(h):
    j = h - 1
    k = 0
    l = 0
    while j > i:
        print(" ", end="")
        j -= 1

    while k <= i:
        print("#", end="")
        k += 1

    print("  ", end="")

    while l <= i:
        print("#", end="")
        l += 1

    print("")