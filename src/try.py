#/usr/bin/python
from ghmm import *

#-----------------------------------------------------------------------------Viterbi Test
obs_states = IntegerRange(1, 3) # Range of the observation.
                                # N.B. the upper limit is not part of a range.
A = [[0.4, 0.6], [0.1, 0.9]]
B = [[0.8, 0.2], [0.1, 0.9]]
pi = [0.98, 0.02]
m = HMMFromMatrices(obs_states, DiscreteDistribution(obs_states), A, B, pi)
print m

obs = EmissionSequence(obs_states, [2, 1, 2])

[states, prob] = m.viterbi(obs)

print(states)
print states.__str__().replace("0", "climb").replace("1", "not climb")
print prob # N.B. prob = log_e(actual_prob)

print "-------------------------------------------------------------------------------------"
#-----------------------------------------------------------------------------Forward test
obs_states = IntegerRange(1, 3) # Range of the observation.
                                # N.B. the upper limit is not pa
A = [[0.7, 0.3], [0.4, 0.6]]
B = [[0.4, 0.6], [0.8, 0.2]]
pi = [0.5, 0.5]
m = HMMFromMatrices(obs_states, DiscreteDistribution(obs_states), A, B, pi)
print m

obs = EmissionSequence(obs_states, [1, 2, 2])

[prob_ditributions, alphas] = m.forward(obs)
for distribution in prob_ditributions:
    print(distribution)
for alpha in alphas:
    print(alpha)

print "-------------------------------------------------------------------------------------"
#-----------------------------------------------------------------------------Backwardward test

def normalize(not_yet_prob):
    if not_yet_prob != [1, 1]:
        return [i / sum(not_yet_prob) for i in not_yet_prob]
    return not_yet_prob


obs_states = IntegerRange(1, 3) # Range of the observation.
                                # N.B. the upper limit is not pa
A = [[0.7, 0.3], [0.3, 0.7]]
B = [[0.9, 0.1], [0.2, 0.8]]
pi = [0.5, 0.5]
m = HMMFromMatrices(obs_states, DiscreteDistribution(obs_states), A, B, pi)
print m

obs_b = EmissionSequence(obs_states, [1, 1, 2, 1])

[forprobs, scale] = m.forward(obs_b)
not_scaled_probs = m.backward(obs_b, scale)
backprobs = list()

for not_scaled_prob in not_scaled_probs:
    backprobs.insert(len(backprobs), normalize(not_scaled_prob))
    #print normalize(not_scaled_prob)

print forprobs
print backprobs

# Smooting
for i in range(0, len(forprobs)):
    [f_1, f_2] = forprobs[i]
    [b_1, b_2] = backprobs[i]
    x = f_1*b_1
    y = f_2*b_2
    print normalize([x, y])


print "-------------------------------------------------------------------------------------"
#----------------------------------------------------------------------------- Baum-Welch algorithm
obs_states = IntegerRange(1, 3) # Range of the observation.
                                # N.B. the upper limit is not pa
A = [[0.7, 0.3], [0.3, 0.7]]
B = [[0.9, 0.1], [0.2, 0.8]]
pi = [0.5, 0.5]
m = HMMFromMatrices(obs_states, DiscreteDistribution(obs_states), A, B, pi)
print m

obs_b = EmissionSequence(obs_states, [2, 1, 1, 2, 2])

m.baumWelch(obs_b)
print m