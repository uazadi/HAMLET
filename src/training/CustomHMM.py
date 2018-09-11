import GlobalVar
from ghmm import *

alphabet = list(GlobalVar.alphabet)
observable = GlobalVar.observable

class CustomHMM:
    def __init__(self,
                 hmm,
                 transition_matrix,
                 emission_matrix,
                 initial_probabilities,
                 obs_states,
                 vocabulary):
        self.hmm = hmm
        self.transition_matrix = transition_matrix
        self.emission_matrix = emission_matrix
        self.initial_probabilities = initial_probabilities
        self.obs_states = obs_states
        self.vocabulary = vocabulary

    def __str__(self):
        value = "Vocabulary:\n"\
              + str(self.vocabulary) \
              + "\n\n\nInitial Probabilities:\n" \
              + str(self.initial_probabilities) \
              + "\n\n\nTransition Matrix: \n"

        for i in range(0, len(self.transition_matrix)):
            value = value \
                    + str(alphabet[i]) \
                    + " -> " \
                    + str(self.transition_matrix[i]) \
                    + "\n"

        value = value + "\n\n\nEmission Matrix: \n"

        for i in range(0, len(self.emission_matrix)):
            value = value \
                    + str(alphabet[i]) \
                    + " -> " \
                    + str(self.emission_matrix[i]) \
                    + "\n"

        return value

    def save_vocabulary(self, file_name):
        voc = open(file_name, 'w')
        voc_set = set(self.vocabulary)
        for word in voc_set:
            voc.write(str(word).replace(" ", "") + "\n")
        voc.close()

    def save_matrix(self, name, matrix, header):
        tr = open(name, 'w')
        for i in header:
            tr.write(str(i) + ";")
        tr.write("\n")
        for i in matrix:
            if type(i) == list:
                for j in i:
                    num = format(j, '.12f')
                    tr.write(num + ";")
                tr.write("\n")
            else:
                num = format(i, '.12f')
                tr.write(num + ";")


    def save_hmm(self, folder):

        if folder is None:
            i = 1
            path = '/home/umberto/Documents/HMMTweetChecker/src'
            folder = path + '/HMM/'
            while os.path.exists(folder):
                folder = path + '/HMM_' + str(i) + '/'
                i = i + 1
            os.makedirs(folder)

        self.save_vocabulary(folder + "vocabulary.txt")
        self.save_matrix(
            folder + "transition_matrix.csv",
            self.transition_matrix,
            alphabet)
        self.save_matrix(
            folder + "emission_matrix.csv",
            self.emission_matrix,
            observable)
        self.save_matrix(
            folder + "initial_probabilities.csv",
            self.initial_probabilities,
            alphabet)


def load_matrix(hmm_dir, name):
    file = open(hmm_dir + name)
    header = file.next()
    matrix = []
    for line in file:
        raw = line.split(";")
        raw.pop()
        raw = [float(x) for x in raw]
        matrix.insert(len(matrix), raw)

    return matrix


def load_vocabulary(hmm_dir):
    file = open(hmm_dir + "vocabulary.txt")
    voc = []
    for line in file:
        voc.insert(len(voc), line.replace("\n", " "))
    return voc


def load(hmm_dir):
    obs_states = IntegerRange(1, len(observable) + 1)
    transition_matrix = load_matrix(hmm_dir, "transition_matrix.csv")
    emission_matrix = load_matrix(hmm_dir, "emission_matrix.csv")
    initial_probabilities = load_matrix(hmm_dir, "initial_probabilities.csv")[0]
    vocabulary = load_vocabulary(hmm_dir)
    model = HMMFromMatrices(obs_states,
                            DiscreteDistribution(obs_states),
                            transition_matrix,
                            emission_matrix,
                            initial_probabilities)

    chmm = CustomHMM(
        model,
        transition_matrix,
        emission_matrix,
        initial_probabilities,
        obs_states,
        vocabulary)

    return chmm

if __name__ == '__main__':
    print load("/home/umberto/Documents/HMMTweetChecker/src/HMM_1/")