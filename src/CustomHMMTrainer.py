def getVocabulary2(file):
    voc = []
    for line in file:
        voc.extend(str(line).split(" "))

    voc = list(set(voc))

    print [(i, voc[i]) for i in range(0, len(voc))]

    return voc