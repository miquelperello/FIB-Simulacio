import numpy as np
import matplotlib.pyplot as plt

N = 10000
mu, sigma = 150, 45
mu2, sigma2 = 10, 45
X1 = gfg = np.random.triangular(2, 10, 16, 10000)
X2 = gfg = np.random.triangular(12, 17, 26, 10000)
X = np.concatenate([X1, X2])

plt.figure(1)
(n, bins, patches) = plt.hist(X)
plt.close(1)
print("Bins:", bins)
print("N:", n)
