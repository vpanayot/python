import math

print('Get first item in a list: [5, 1, 34]')
print((lambda lst: lst[0])([5, 1, 34]))

print('Apply logistic function to each element in a list: [-3, -5, 1, 4]')
print(list(map(lambda x: round(1 / (1 + math.exp(-x)), 4) ,[-3, -5, 1, 4])))