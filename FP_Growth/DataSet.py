
class DatasetProcessing():

    db = []
    file = None

    def __init__(self, fname):
        self.file = open(fname, 'r')
        pass

    def preprocess(self):
        DatasetProcessing.db = []
        for seq in self.file:
            tns = seq.strip().split()
            # print(tns)
            tmp_tns = []
            for itm in tns:
                tmp_tns.append(int(itm))
            tmp_tns.sort()
            # print(tmp_tns)
            self.db.append(tmp_tns)


