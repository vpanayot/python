def average(*args):
    sum = 0
    for i in args:
        sum += i
    return  sum / len(args)

print(average(2, 5, 12, 54))
print(average(9.3, 65.2, -6))