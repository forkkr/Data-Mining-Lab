import copy
import time

import numpy as np
from sklearn.model_selection import KFold
from DecisionTree.DT__init__ import DT_INIT
from BayesianClassification.Bayesian import BayesianClassifier


class CV():

    def measures(self, Total, accurate, p, tp, fp):

        accuracy, precision, recall, f_score = 0, -1, -1, -1
        # print(accuracy, precision, recall, f_score)

        accuracy = accurate * 100.0 / Total

        if p and tp:
            precision = tp * 100.0 / (tp + fp)
            recall = tp * 100.0 / p
            f_score = 2 * precision * recall / (precision + recall)

        return [accuracy, precision, recall, f_score]

    def cross_validation(self, kfold, datasetName, num_of_instances, datafilename, attrifile, reverse_order, true_class, pruning_threshold):
        X = np.array([x for x in range(1, num_of_instances+1)])

        TRUE_CLASS = true_class
        DATASET_NAME = datasetName
        resultFile = open('result_new.csv', 'a')
        header = 'Dataset, Positive Class,k,DT_threshold,' \
                 'Accuracy DT,Accuracy Bayesian,' \
                 'Precision DT, Precision Bayesian,' \
                 'Recall DT, Recall Bayesian,' \
                 'F-score DT, F-score Bayesian,' \
                 'Runtime DT, Runtime Bayesian\n'

        # resultFile.write(header)

        kf = KFold(n_splits=kfold, random_state=None, shuffle=True)
        kf.get_n_splits(X)
        # trainfile = open('train.data', 'w')
        # testfile = open('test.data', 'w')
        # datafile = open(datafile, 'r')

        dt_total = []
        dt_correct = []
        dt_p = []
        dt_tp = []
        dt_fp = []
        dt_time = []
        b_total = []
        b_correct = []
        b_p = []
        b_tp = []
        b_fp = []
        b_time = []

        for train_index, test_index in kf.split(X):
            trainfile = open('train.data', 'w')
            testfile = open('test.data', 'w')
            datafile = open(datafilename, 'r')
            # print("TRAIN:", len(train_index), "TEST:", len(test_index), 'Ratio: ', len(train_index) / len(test_index))
            tmp_list = [X[i] for i in train_index]
        train_index = copy.deepcopy(tmp_list)
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

        total_dt, correct_dt, P_dt, TP_dt, FP_dt, time_dt = DT_INIT().run_DT_model('train.data', 'test.data',
                                                                                   attrifile, reverse_order,
                                                                                   TRUE_CLASS, pruning_threshold)
        # total_dt, correct_dt, P_dt, TP_dt, FP_dt, time_dt = 1, 1, 1, 1, 1, 1
        print('DT: ', total_dt, correct_dt, P_dt, TP_dt, FP_dt, round(time_dt, 4))
        dt_total.append(total_dt)
        dt_correct.append(correct_dt)
        dt_p.append(P_dt)
        dt_tp.append(TP_dt)
        dt_fp.append(FP_dt)
        dt_time.append(time_dt)

        print(round(correct_dt / total_dt, 4), ' Accuracy of DT')

        # print('')

        t1 = time.time()
        bayes = BayesianClassifier('train.data', attrifile, reverse_order, TRUE_CLASS)
        t2 = time.time()
        total_b, correct_b, P_b, TP_b, FP_b, accuracy, precision, recall, fscore = bayes.test_run('test.data')
        t3 = time.time()
        time_b = t3 - t1

        print('Bayes: ', total_b, correct_b, P_b, TP_b, FP_b, round(time_b, 4))

        b_total.append(total_b)
        b_correct.append(correct_b)
        b_p.append(P_b)
        b_tp.append(TP_b)
        b_fp.append(FP_b)
        b_time.append(time_b)

        print('---------------------------------')

        print('SUMMARY of ', datafilename)
        dt_info = self.measures(sum(dt_total), sum(dt_correct),
                                sum(dt_p), sum(dt_tp), sum(dt_fp))
        dt_info.append(sum(dt_time))

        print('DT', self.measures(sum(dt_total), sum(dt_correct),
                                  sum(dt_p), sum(dt_tp), sum(dt_fp)),
              'Time: ', sum(dt_time))
        print('Bayes', self.measures(sum(b_total), sum(b_correct),
                                     sum(b_p), sum(b_tp), sum(b_fp)),
              'Time: ', sum(b_time))

        b_info = self.measures(sum(b_total), sum(b_correct),
                               sum(b_p), sum(b_tp), sum(b_fp))
        b_info.append(sum(b_time))

        # print(dt_info)
        # print(b_info)

        csv_data = DATASET_NAME + ',' + TRUE_CLASS + ',' + str(kfold) + ',' + str(pruning_threshold)
        for i in range(0, len(dt_info)):
            csv_data += ',' + str(dt_info[i]) + ',' + str(b_info[i])
        csv_data += '\n'

        resultFile.write(csv_data)
        resultFile.close()
