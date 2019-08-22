import copy

from Apriori.DataSet import DatasetProcessing as dsp


class AprioriAlgorithm():
    itms = list()
    threshold = 0.0
    fname = None
    cur_trns = list()
    local_set = []
    candidate = []
    cur_label = None
    root_node = None
    cur_local_pattern = []
    total_pattern = 0

    def __init__(self, threshold):
        self.threshold = threshold*len(dsp.db)
        pass

    def apriori_algorithm(self):
        L1, C2 = self.init_fs_gen()
        self.total_pattern += len(L1)
        # print('L1: item with support count-')
        # for l1 in L1:
        #     print(l1[0], ' : ', l1[1])
        C2.sort()
        # print('C2:')
        # for c2 in C2:
        #     print(c2)
        flag = True
        self.candidate = C2
        self.cur_label = 2
        print('Candidate Set for Label '+ str(self.cur_label)+' :')
        self.root_node = Node()
        while flag :
            for can in self.candidate:
                print(can)
                self.build(self.root_node, can, 0)

            for i in range(0, len(dsp.db)):
                self.support_update(self.root_node, i)

            # print('Traversing: ')
            # self.traverse_trie(self.root_node, [])

            self.frequent_set_generation(self.root_node)

            # print('Traversing: ')
            # self.traverse_trie(self.root_node, [])

            print('Frequent Pattern for Label', self.cur_label,' :')
            tot_fs = self.print_FS(self.root_node, [])
            self.total_pattern += tot_fs
            print(tot_fs, self.cur_label)
            if tot_fs <= self.cur_label:
                break
            self.local_set = []
            self.joining(self.root_node, [], 0)
            # print('Pre L' + str(self.cur_label) + ' :')
            # for ls in self.local_set:
            #     print(ls)

            self.candidate = []
            self.candidate_generation()
            self.cur_label += 1
            print('Candidate Set for Label '+ str(self.cur_label)+' :')
        return self.total_pattern
            # flag -=1

    def build(self, cur_node, seq, pos):
        if pos >= len(seq):
            return
        if seq[pos] in cur_node.dscnts:
            cur_node.dscnts[seq[pos]].support = 0
            self.build(cur_node.dscnts[seq[pos]], seq, pos+1)
        else:
            new_node = Node()
            cur_node.dscnts[seq[pos]] = new_node
            # print(seq[pos], ' at build')
            new_node.label = seq[pos]
            new_node.support = 0
            self.build(new_node, seq, pos+1)

    def support_update(self, cur_node, trn_id):
        # print(dsp.db[trn_id], type(cur_node.label))
        got = False
        if cur_node.label is not None:
            # print(cur_node.label, ' cur_node label at support_update')
            l = 0
            r = len(dsp.db[trn_id])-1
            got = False
            while l <= r:
                m = (l+r) // 2
                if int(dsp.db[trn_id][m]) == cur_node.label:
                    cur_node.support += 1
                    got = True
                    break
                elif int(dsp.db[trn_id][m]) < cur_node.label:
                    l = m + 1
                else:
                    r = m-1
        if got or (cur_node.label is None):
            for dscnt in cur_node.dscnts:
                self.support_update(cur_node.dscnts[dscnt], trn_id)

    def traverse_trie(self, cur_node, cur_itms):
        if cur_node.label is not None:
            cur_itms.append(cur_node.label)
        if cur_node.marker == True:
            print(cur_itms, ': ', cur_node.support)
        for dscnt in cur_node.dscnts:
            self.traverse_trie(cur_node.dscnts[dscnt], copy.deepcopy(cur_itms))
        return

    def init_fs_gen(self):
        itms_dic = dict()
        for itms in dsp.db:
            for itm in itms:
                if itm not in itms_dic:
                    itms_dic[itm] = 1
                else:
                    itms_dic[itm] += 1
        L1 = list()
        for itm in itms_dic:
            if itms_dic[itm] >= self.threshold:
                L1.append([int(itm), itms_dic[itm]])
        L1.sort()
        C2 = list()
        for i in range(0, len(L1)):
            for j in range(i+1, len(L1)):
                C2.append([L1[i][0], L1[j][0]])
        return L1, C2

    def candidate_generation(self):
        for ls in self.local_set:
            self.cur_local_pattern = ls
            ret = self.apriori_pruning()
            if ret is True:
                self.candidate.append(ls)
        return

    def checking_subpatterns(self, cur_node, cur_set, pos):
        if pos >= len(cur_set):
            return True
        if cur_set[pos] not in cur_node.dscnts:
            return False
        return self.checking_subpatterns(cur_node.dscnts[cur_set[pos]], cur_set, pos+1)

    def apriori_pruning(self):
        for i in range(0, len(self.cur_local_pattern)):
            tmp_cur = copy.deepcopy(self.cur_local_pattern)
            del tmp_cur[i]
            ret = self.checking_subpatterns(self.root_node, tmp_cur, 0)
            if ret is False:
                return False
        return True

    def frequent_set_generation(self, cur_node):
        tmp_dscnts = copy.deepcopy(cur_node.dscnts)
        cur_node.dscnts = dict()
        if cur_node.label is not None and cur_node.support < self.threshold:
            cur_node.marker = False
        child_no = 0
        for dscnt in tmp_dscnts:
            ret = self.frequent_set_generation(tmp_dscnts[dscnt])
            if ret > 0:
                child_no += ret
                cur_node.dscnts[dscnt] = tmp_dscnts[dscnt]
        return child_no + cur_node.marker

    def print_FS(self, cur_node, cur_set):
        if cur_node.label is not None:
            cur_set.append(cur_node.label)
            if len(cur_set) == self.cur_label:
                print(cur_set, " : ", cur_node.support)
                return 1
        cnt = 0
        for dscnt in cur_node.dscnts:
            cnt += self.print_FS(cur_node.dscnts[dscnt], copy.deepcopy(cur_set))
        return cnt

    def joining(self, cur_node, cur_set, depth):
        if cur_node.label is not None:
            cur_set.append(cur_node.label)
        if depth == self.cur_label - 1:
            itms = list(cur_node.dscnts.keys())
            # print(itms)
            itms.sort()
            # print(itms)
            for i in range(0, len(itms)):
                for j in range(i+1, len(itms)):
                    self.local_set.append(cur_set+[itms[i], itms[j]])
            return
        for dscnt in cur_node.dscnts:
            tmp_cur_set = copy.deepcopy(cur_set)
            self.joining(cur_node.dscnts[dscnt], tmp_cur_set, depth+1)


class Node():

    def __init__(self):
        self.label = None
        self.support = 0.0
        self.dscnts = dict()
        self.marker = True
        self.depth = None
