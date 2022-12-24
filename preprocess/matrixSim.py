import numpy as np
from numpy.linalg import norm
from numpy import dot

A = np.array([0.1,0.2,2])
B = np.array([0.4,0.2,4])
i=0
while(i<100000):
    # cosine = np.sum(A*B, axis=1)/(norm(A, axis=1)*norm(B, axis=1))
    cosine = cos_sim = dot(A, B)/(norm(A)*norm(B))
    print("Cosine Similarity:\n", cosine)
    i+=1
    break

