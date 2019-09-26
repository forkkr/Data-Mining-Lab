import math,random


class BayesianClassifier:

    db = list()
    dbSize = 0

    ci_tids = dict()
    ci_size = dict()
    attr_labels = list()
    attr_type = list()
    attr_vals = dict()
    sup_xk_ci = dict()
    conts_attr_info = dict()

    def __init__(self, dataset, attr_file):
        self.dataset_file = open(dataset, 'r')
        self.attr_file = open(attr_file, 'r')

        self.read_and_process()

        self.dataset_file.close()
        self.attr_file.close()

        class_labels = self.ci_tids.keys()
        for c in class_labels:
            # print(c,self.ci_tids[c],len(self.ci_tids[c]), round(len(self.ci_tids[c])/(self.dbSize * 1.0),4))
            self.ci_size[c] = len(self.ci_tids[c])

        # aid_xk_ci = self.sup_xk_ci.keys()
        # for axc in aid_xk_ci:
        #     cls = axc[2]
        #     cls_size = len(self.ci_tids[cls])
        #     # print(cls,cls_size)
        #     print(axc,round(self.sup_xk_ci[axc]*1.0/cls_size,4))
        #
        # attrs = self.attr_vals.keys()
        # for a in attrs:
        #     print(self.attr_labels[a],self.attr_vals[a])

        self.laplacian_correction()

        for attr_id in range(0,len(self.attr_labels)):
            if self.attr_type[attr_id] == 1:
                vals = self.attr_vals[attr_id]
                values = []
                for v in vals:
                    values.append(float(v))
                mean = self.mean(values)
                stddev = self.stddev(values)
                self.conts_attr_info[attr_id] = (mean, stddev)
        # print(self.conts_attr_info)
        # print(self.gaussian_dist(41,self.conts_attr_info[3][0],self.conts_attr_info[3][1]))

    def read_and_process(self):

        for attr_info in self.attr_file:
            attr_info = attr_info.split(' ')
            self.attr_labels.append(str(attr_info[0]))
            self.attr_type.append(int(attr_info[1]))

        tid = 0
        for entry in self.dataset_file:
            tid += 1
            entry = entry.strip().replace('\n', '').replace('\r', '')
            xk_values = entry.split(',')
            self.db.append(xk_values)
            self.dbSize += 1

            ci = xk_values[len(xk_values)-1]
            ci_tuples = self.ci_tids.get(ci)
            if ci_tuples is None:
                ci_tuples = list()
            ci_tuples.append(tid)
            self.ci_tids[ci] = ci_tuples

            for i in range(0,len(xk_values)):
                a_id = i
                a_label = self.attr_labels[i]
                a_typ = self.attr_type[i]
                a_val = xk_values[i]

                # print(a_label,a_val,end='; ')

                l = self.attr_vals.get(a_id)
                if l is None:
                    l = list()
                if a_typ == 0:
                    if a_val not in l:
                        l.append(a_val) #no duplicate entry in categorical data
                else:
                    l.append(a_val) #allow duplicate to measure mean and variance
                self.attr_vals[a_id] = l

                if a_typ == 0:
                    '''categorical'''
                    support = self.sup_xk_ci.get((a_id, a_val, ci), 0)
                    self.sup_xk_ci[(a_id, a_val, ci)] = support + 1
            # print('-')


    def laplacian_correction(self):
        aid_xk_ci = self.sup_xk_ci.keys()

        classes = self.ci_tids.keys()
        for ci in classes:
            for a_id in range(0, len(self.attr_labels)-1):
                need_correction = False
                if self.attr_type[a_id] == 0:
                    a_vals = self.attr_vals[a_id]
                    for xk in a_vals:
                        if (a_id,xk,ci) not in aid_xk_ci:
                            # self.sup_xk_ci[(a_id,xk,ci)] = 1
                            need_correction = True
                            break

                    if need_correction:
                        for xk in a_vals:

                            if (a_id, xk, ci) not in aid_xk_ci:
                                self.sup_xk_ci[(a_id,xk,ci)] = 1
                            else:
                                self.sup_xk_ci[(a_id, xk, ci)] = self.sup_xk_ci[(a_id,xk,ci)]+1

                            self.ci_size[ci] = self.ci_size[ci]+1

        # for axc in aid_xk_ci:
        #     cls = axc[2]
        #     cls_size = self.ci_size[cls]
        #     print(cls,cls_size)
        #     print(axc,round(self.sup_xk_ci[axc]*1.0/cls_size,4))

    def test_run(self,testFile):

        with open(testFile,'r') as tf:
            for line in tf:
                line = line.replace('\n', '').replace('\r', '').strip()
                vals = line.split(',')
                actual = vals[len(vals)-1]
                predicted  = self.classify(vals)
                if actual!=predicted:
                    print('__________WRONG')
                # print(actual, predicted)

    def classify(self, vals):

        actual_cls = vals[len(vals)-1]

        predicted_cls = dict()

        classes = self.ci_tids.keys()
        for ci in classes:
            cls_size = self.ci_size[ci]
            p_ci = cls_size*1.0/self.dbSize
            prob = p_ci
            for a_id in range(0,len(vals)-1):
                # print(self.attr_labels[a_id])
                if self.attr_type[a_id] == 0:
                    p_xk_ci = self.sup_xk_ci[(a_id,vals[a_id],ci)]*1.0/cls_size
                else:
                    p_xk_ci = self.gaussian_dist(float(vals[a_id]),self.conts_attr_info[a_id][0],self.conts_attr_info[a_id][1])
                prob = prob * p_xk_ci
            predicted_cls[ci] = prob
            # print(prob)

        v = list(predicted_cls.values())
        k = list(predicted_cls.keys())
        print(vals, k[v.index(max(v))])
        return k[v.index(max(v))]

    def gaussian_dist(self, x, mu, dev):
        # pi = 3.14159 # or math
        # print(math.pi)
        # print(math.e)
        # print(math.pow(math.e,-2))
        prob = 1.0 / (math.sqrt(2*math.pi) * dev) * math.pow(math.e, (- (x-mu)*(x-mu) / (2*dev*dev)))
        return prob

    def mean(self, data):
        """Return the sample arithmetic mean of data."""
        n = len(data)
        if n < 1:
            raise ValueError('mean requires at least one data point')
        return sum(data) / n  # in Python 2 use sum(data)/float(n)

    def _ss(self, data):
        """Return sum of square deviations of sequence data."""
        c = self.mean(data)
        ss = sum((x - c) ** 2 for x in data)
        return ss

    def stddev(self, data, ddof=0):
        """Calculates the population standard deviation
        by default; specify ddof=1 to compute the sample
        standard deviation."""
        n = len(data)
        if n < 2:
            raise ValueError('variance requires at least two data points')
        ss = self._ss(data)
        pvar = ss / (n - ddof)
        return pvar ** 0.5

