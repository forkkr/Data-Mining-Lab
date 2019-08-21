
class DatasetProcessing():

    db = []
    file = None

    def __init__(self, fname):
        self.file = open(fname, 'r')
        pass

    def preprocess(self):
        for seq in self.file:
            tns = seq.strip().split()
            # print(tns)
            self.db.append(tns)


