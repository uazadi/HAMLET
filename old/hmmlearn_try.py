import numpy as np
from hmmlearn import hmm

n_components = 2   # ['Rainy', 'Sunny']
n_features = 2     # ['walk', 'shop', 'clean']
h = hmm.MultinomialHMM(n_components)
h.n_features = n_features
h.startprob_ = np.array([0.98, 0.02])
h.transmat_ = np.array([[0.4, 0.6], [0.1, 0.9]])
h.emissionprob_ = np.array([[0.8, 0.2], [0.1, 0.9]])

X = [[1], [0], [1]]
logprob, state_sequence = h.decode(X, algorithm="viterbi")
logprob = round(np.exp(logprob), 5)
print(logprob)
print(state_sequence)

print(h.startprob_)
print(h.transmat_)
print(h.emissionprob_)

h.fit([[1], [1], [0], [1]])

print(h.startprob_)
print(h.transmat_)
print(h.emissionprob_)

(a, b) = h.sample(5)
print a
print b