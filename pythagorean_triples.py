#Holds Pythagorean triples count
pt_count = 0

for c in range(1, 48):
    for b in range(1, c):
        for a in range(1, b):
            if a * a + b * b == c * c:
                #print('{}, {}, {}'.format(a,b,c))
                print('{:3d}{:3d}{:3d}'.format(a,b,c))
                pt_count += 1

print(f'Pythagorean triples count: {pt_count}')
