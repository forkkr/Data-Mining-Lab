import numpy as np
from sklearn.model_selection import KFold
from DecisionTree.DT__init__ import DT_INIT


class CV():

    def cross_validation(self, kfold, num_of_instances, datafilename, attrifile, reverse_order):
        X = np.array([x for x in range(1, num_of_instances+1)])

        kf = KFold(n_splits=kfold, random_state=None, shuffle=True)
        kf.get_n_splits(X)
        # trainfile = open('train.data', 'w')
        # testfile = open('test.data', 'w')
        # datafile = open(datafile, 'r')
        for train_index, test_index in kf.split(X):
            trainfile = open('train.data', 'w')
            testfile = open('test.data', 'w')
            datafile = open(datafilename, 'r')
            print("TRAIN:", len(train_index), "TEST:", len(test_index), 'Ratio: ', len(train_index)/len(test_index))

            tuple_no = 1
            for tuple_info in datafile:
                if tuple_no in train_index:
                    # print(tuple_no, tuple_info)
                    trainfile.write(tuple_info)
                else:
                    testfile.write(tuple_info)
                tuple_no += 1

            trainfile.close()
            testfile.close()
            datafile.close()

            DT_INIT().run_DT_model('train.data', 'test.data', attrifile, reverse_order)
            print('///////////')
