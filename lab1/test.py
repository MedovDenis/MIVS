import numpy as np

a = 2
n = 15
N = 10000

r = np.random.sample(N)
x = np.sort([a * np.sqrt(1 - (1 - i)**2) for i in r])

min, max = np.min(x), np.max(x)

# n = int(np.log2(N)) + 1

p = [min]
p_next = np.sqrt(a**2 - (np.sqrt(a**2 - min**2) - a/n)**2)

while(p_next < max):
    p.append(p_next)
    p_next = np.sqrt(a**2 - (np.sqrt(a**2 - p_next**2) - a/n)**2)
    print(p_next)
    if (len(p) >= n): break
p.append(2)

print(p)
print(len(p))
