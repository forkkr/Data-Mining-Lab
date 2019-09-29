import math, statistics

import numpy as np


class BayesianClassifier:

    def __init__(self, dataset, attr_file, reverse_order, true_class):
        self.db = list()
        self.dbSize = 0

        self.ci_tids = dict()
        self.ci_size = dict()
        self.attr_labels = list()
        self.attr_type = list()
        self.attr_vals = dict()

        self.attr_ci_vals = dict()
        self.mean_std_dict = dict()
        self.sup_xk_ci = dict()
        self.conts_attr_info = dict()
        self.reverse_order = reverse_order
        self.true_class = true_class
        self.false_class = None

        self.dataset_file = open(dataset, 'r')
        self.attr_file = open(attr_file, 'r')

        self.read_and_process()

        self.dataset_file.close()
        self.attr_file.close()

        class_labels = self.ci_tids.keys()
        for c in class_labels:
            # print(c, self.ci_tids[c], len(self.ci_tids[c]), round(len(self.ci_tids[c]) / (self.dbSize * 1.0), 4))
            self.ci_size[c] = len(self.ci_tids[c])

        # aid_xk_ci = self.sup_xk_ci.keys()
        # for axc in aid_xk_ci:
        #     cls = axc[2]
        #     cls_size = len(self.ci_tids[cls])
        #     # print(cls,cls_size)
        #     print(axc,round(self.sup_xk_ci[axc]*1.0/cls_size,4))
        #
        attrs = self.attr_vals.keys()
        # for a in attrs:
        #     print(self.attr_labels[a], self.attr_vals[a])

        # for attr_id in range(0, len(self.attr_labels)):
        #     if self.attr_type[attr_id] == 1:
        #         vals = self.attr_vals[attr_id]
        #         values = []
        #         for v in vals:
        #             # print(v)
        #             values.append(float(v))
        #
        #         m, s = self.find_m_s(values)
        #         print(self.attr_labels[attr_id], values,m,s)
        #         self.conts_attr_info[attr_id] = (m, s)

        for attr_id in range(0, len(self.attr_labels)):
            if self.attr_type[attr_id] == 1:
                for ci in class_labels:
                    value_array = self.attr_ci_vals[(attr_id,ci)]
                    # print('Calc m,s:',self.attr_labels[attr_id],ci,value_array)
                    mean , stddev = self.find_m_s(value_array)
                    self.mean_std_dict[(attr_id,ci)] = (mean, stddev)

        # print(self.mean_std_dict)

    def read_and_process(self):

        for attr_info in self.attr_file:
            attr_info = attr_info.split(' ')
            self.attr_labels.append(str(attr_info[0]))
            self.attr_type.append(int(attr_info[1]))

        if self.reverse_order == 1:
            self.attr_labels.reverse()
            self.attr_type.reverse()
            # print(self.attr_labels)
            # print(self.attr_type)

        tid = 0
        for entry in self.dataset_file:

            entry = entry.strip().replace('\n', '').replace('\r', '')
            if entry == '' or entry is None:
                break
            xk_values = entry.split(',')

            if '?' in xk_values:
                # print('missing values', xk_values)
                continue

            if len(xk_values) != len(self.attr_labels):
                continue

            if self.reverse_order == 1:
                xk_values.reverse()
                # print('After', xk_values)

            self.db.append(xk_values)
            self.dbSize += 1

            ci = xk_values[len(xk_values) - 1]
            ci_tuples = self.ci_tids.get(ci)
            if ci_tuples is None:
                ci_tuples = list()
            ci_tuples.append(tid)
            self.ci_tids[ci] = ci_tuples

            for i in range(0, len(xk_values)):
                a_id = i
                a_label = self.attr_labels[i]
                a_typ = self.attr_type[i]
                a_val = xk_values[i]

                # print(a_label, a_val, end='; ')

                l = self.attr_vals.get(a_id)

                if l is None:
                    l = list()
                if a_typ == 0:
                    if a_val not in l:
                        l.append(a_val)  # no duplicate entry in categorical data
                else:
                    l.append(a_val)  # allow duplicate to measure mean and variance
                self.attr_vals[a_id] = l

                if a_typ == 1:
                    attr_value_list = self.attr_ci_vals.get((a_id, ci))
                    if attr_value_list is None:
                        attr_value_list = list()
                    attr_value_list.append(float(a_val))
                    self.attr_ci_vals[(a_id,ci)] = attr_value_list



                if a_typ == 0:
                    '''categorical'''
                    support = self.sup_xk_ci.get((a_id, a_val, ci), 0)
                    self.sup_xk_ci[(a_id, a_val, ci)] = support + 1
            tid += 1
            # print('-')

    def test_run(self, testFile):

        total = 0
        correct = 0
        TP = 0
        FP = 0
        P = 0
        precision = -1.0
        recall = -1.0
        F_score = -1.0
        with open(testFile, 'r') as tf:
            for line in tf:
                line = line.replace('\n', '').replace('\r', '').strip()
                vals = line.split(',')
                if '?' in vals:
                    # print('missing value in test')
                    # print(vals)
                    continue

                if self.reverse_order == 1:
                    vals.reverse()

                actual = vals[len(vals) - 1]

                if actual == self.true_class:
                    # print('P')
                    P += 1

                predicted = self.classify(vals)
                # print(vals,predicted)
                # print('')

                total += 1

                # print(actual, predicted, actual == predicted)
                #s
                if actual != predicted:
                    if predicted == self.true_class:
                        # print('FP')
                        FP += 1
                    # print('__________WRONG')
                # print(actual, predicted)
                else:
                    if predicted == self.true_class:
                        # print('TP')
                        TP += 1
                    correct += 1

        print('total', total, 'correct', correct, 'P', P, 'TP', TP, 'FP', FP)

        if TP and P:
            precision = (TP * 1.0) / (TP + FP)
            recall = TP * 1.0 / P
            F_score = 2 * precision * recall / (precision + recall)

        # print('accuracy', round(correct * 1.0 / total, 4), 'precision', round(precision, 4),
        #       'recall', round(recall, 4), 'F-score', round(F_score, 4))

        return total, correct, P, TP, FP, round(correct * 1.0 / total, 4), round(precision, 4), round(recall, 4), round(
            F_score, 4)
        pass

    def classify(self, vals):

        predicted_cls = dict()

        classes = self.ci_tids.keys()
        for ci in classes:
            cls_size = self.ci_size[ci]
            # print(ci, cls_size, self.dbSize)
            p_ci = cls_size * 1.0 / self.dbSize
            prob = p_ci
            # print(ci,p_ci)
            for a_id in range(0, len(vals) - 1):
                # print(self.attr_labels[a_id])
                if self.attr_type[a_id] == 0:
                    # p_xk_ci = self.sup_xk_ci[(a_id,vals[a_id],ci)]*1.0/cls_size
                    supp = self.sup_xk_ci.get((a_id, vals[a_id], ci), 0)
                    if supp == 0:
                        supp = 1
                        # print('******', self.attr_labels[a_id], self.attr_vals[a_id])
                        p_xk_ci = supp * 1.0 / (cls_size + len(self.attr_vals[a_id]))
                    else:
                        p_xk_ci = supp * 1.0 / cls_size
                else:
                    mean,stddev  = self.mean_std_dict[(a_id,ci)]
                    p_xk_ci = self.gauss(float(vals[a_id]), mean, stddev)
                    # print(float(vals[a_id]), mean, stddev, p_xk_ci)
                    # p_xk_ci = self.g(float(vals[a_id]), self.conts_attr_info[a_id][0], self.conts_attr_info[a_id][1])
                prob = prob * p_xk_ci
                # print('Testing',vals[a_id], p_xk_ci,ci, prob)
            predicted_cls[ci] = prob
            # print('')
            # print(prob)

        # print(predicted_cls)
        # print('')

        v = list(predicted_cls.values())
        k = list(predicted_cls.keys())
        # print(vals, k[v.index(max(v))], round(predicted_cls[k[v.index(max(v))]] * 100, 5), '%')
        return k[v.index(max(v))]

    def find_m_s(self, data):
        return np.mean(data),np.std(data)
        # return statistics.mean(data), statistics.stdev(data)

    def gauss(self, x, m, sd):
        dist = 0
        if sd != 0:
            dist = 1.0 / (sd * np.sqrt(2 * np.pi)) * np.exp(- (x - m) ** 2 / (2 * sd ** 2))
        return dist

    def g(self, x, m, s):
        a1 = math.sqrt(2 * math.pi) * s
        a1 = 1.0 / a1
        a2 = (x - m) ** 2
        a2 /= 2 * (s ** 2)
        a2 = -a2
        ret = a1 * math.exp(a2)
        return ret
