q = input("Text:")

n = len(q)
l = 0
for c in q:
    if c.isalpha():
        l += 1
w = len(q.split())

k = 0
s = 0

while k < n:
    if ord(q[k]) == 46 or ord(q[k]) == 33 or ord(q[k]) == 63:
        s += 1
        k += 1
    else:
        k += 1
L = (l / w) * 100

S = (s / w) * 100

index = 0.0588 * L - 0.296 * S - 15.8

grade = round(index)

if grade < 1:
    print("Before Grade 1")
elif grade > 16:
    print("Grade 16+")
else:
    print("Grade", +grade)