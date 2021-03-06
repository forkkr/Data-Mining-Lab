import copy
import time

from Apriori.DataSet import DatasetProcessing as dsp


class AprioriAlgorithm():
    itms = list()
    threshold = 0.0
    fname = None
    cur_trns = list()
    local_set = []
    candidate = []
    cur_level = None
    root_node = None
    cur_local_pattern = []
    total_pattern = 0
    cur_level_joining_candidate_nodes = []
    joining_count = 0
    candidate_count = 0
    pattern_count = 0

    total_candidates=0

    def __init__(self, threshold):
        self.threshold = threshold*len(dsp.db)
        pass

    def apriori_algorithm(self):

        t1 = time.time()

        L1, C2 = self.init_fs_gen()
        self.total_pattern += len(L1)
        self.total_candidates += len(L1)
        self.total_candidates+=len(C2)
        # print('After joining for Label ' + str(1) + ' : ' + str(len(L1)))
        # print('After pruning for Label ' + str(1) + ' : ' + str(len(L1)))
        # print('Frequent Patterns for Label ' + str(1) + ' : ' + str(len(L1)))

        # print('L1: item with support count-')
        # for l1 in L1:
        #     print(l1[0], ' : ', l1[1])
        # C2.sort()
        # print('C2:')
        # for c2 in C2:
        #     print(c2)

        pfmt = '{0:5}  | {1:15} | {2:15} | {3:15}'
        print('_______', '_________________', '_________________', '_________________')
        print(pfmt.format('Level', 'After Joining', 'After Pruning', 'Frequent Patterns'))
        print('_______', '_________________', '_________________', '_________________')
        print(pfmt.format('L1', len(L1), len(L1), len(L1)))

        flag = True
        self.candidate = C2
        self.cur_level = 2
        # print('Candidate Set for Label ' + str(self.cur_level) + ' :')
        # print('After joining for Label ' + str(self.cur_level) + ' : ' + str(len(self.candidate)))
        # print('After pruning for Label ' + str(self.cur_level) + ' : ' + str(len(self.candidate)))

        print_data = ['L'+str(self.cur_level)]
        print_data.append(len(self.candidate))
        print_data.append(len(self.candidate))

        self.root_node = Node()
        for can in self.candidate:
            self.build(self.root_node, can, 0)

        while flag :
            # tmp_time1 = time.time()
            for trns in dsp.db:
                self.support_update(self.root_node, trns)
                # self.updateSupport(self.root_node, trns, 0)

            # tmp_time2 = time.time()
            # print(tmp_time2 - tmp_time1, ': time for support update')

            # print('Traversing: ')
            # self.trie_traversal(self.root_node, [])

            # tmp_time1 = time.time()
            self.pattern_count = 0
            self.frequent_set_generation(self.root_node, 0)

            # tmp_time2 = time.time()
            # print(tmp_time2 - tmp_time1, ': time for FPG')

            # print(' After deletion Traversing: ')
            # self.trie_traversal(self.root_node, [])

            tot_fp = self.pattern_count
            self.total_pattern += tot_fp
            # print(tot_fp)
            # print('Frequent Patterns for Label',self.cur_level, ':', tot_fp)

            print_data.append(tot_fp)
            print(pfmt.format(*print_data))

            if tot_fp < self.cur_level:
                print('patterns', tot_fp,'<',self.cur_level)
                break

            self.candidate_count = 0
            self.joining_count = 0

            # tmp_time1 = time.time()
            self.joining(self.root_node, [], 0)

            # print('After Joining')
            # self.trie_traversal(self.root_node, [])

            self.after_joining_deletion(self.root_node, 0)

            # print('After Deletion')
            # self.trie_traversal(self.root_node, [])

            # tmp_time2 = time.time()
            # print(tmp_time2 - tmp_time1, ': time for joining')

            self.cur_level += 1
            # print('After joining for Level ' + str(self.cur_level) + ' : ' + str(self.joining_count))
            # print('After pruning for Label ' + str(self.cur_level) + ' : ' + str(self.candidate_count ))
            print_data = list()
            print_data.append('L'+str(self.cur_level))
            print_data.append(self.joining_count)
            print_data.append(self.candidate_count)
            self.total_candidates += self.candidate_count

        t2 = time.time()

        print('_______', '_________________', '_________________', '_________________')

        print('Total Candidates Generated: ',self.total_candidates)
        print('Total Patterns Found: ', self.total_pattern)
        print('Time Required: ',round(t2-t1,4))
        return [self.total_candidates,self.total_pattern,round(t2-t1,4)]

    def build(self, cur_node, seq, pos):
        if pos >= len(seq):
            return
        if seq[pos] in cur_node.dscnts:
            dscnt_node = cur_node.dscnts[seq[pos]]
            dscnt_node.support = 0
            dscnt_node.marker = False
            self.build(cur_node.dscnts[seq[pos]], seq, pos+1)
        else:
            new_node = Node()
            cur_node.dscnts[seq[pos]] = new_node
            new_node.label = seq[pos]
            new_node.support = 0
            new_node.marker = False
            self.build(new_node, seq, pos+1)

    def support_update(self, cur_node, trn):
        cur_node.marker = False
        for dscnt in cur_node.dscnts:
            dscnt_node = cur_node.dscnts[dscnt]
            if dscnt_node.label in trn:
                dscnt_node.support += 1
                self.support_update(dscnt_node, trn)

    def find_itm(self, cur_lbl, cur_trn, l, r):
        while l <= r:
            m = (l + r) // 2
            if dsp.db[cur_trn][m] == cur_lbl:
                return m
            elif dsp.db[cur_trn][m] < cur_lbl:
                l = m + 1
            else:
                r = m - 1
        return l

    def updateSupport(self, cur_node, itemList, pos):
        # print(cur_node.label, ' at US')
        if pos >= len(itemList):
            return
        cur_pos = pos
        # print(cur_node.dscnts.keys())
        for dscnt in sorted(cur_node.dscnts):
            dscnt_node = cur_node.dscnts[dscnt]
            # cur_pos = pos
            # print(dscnt_node.label, cur_pos,' Dscnt label')
            while cur_pos < len(itemList):
                if itemList[cur_pos] == dscnt_node.label:
                    dscnt_node.support += 1
                    cur_pos += 1
                    self.updateSupport(dscnt_node, itemList, cur_pos)
                    break
                elif itemList[cur_pos] < dscnt_node.label:
                    cur_pos += 1
                else:
                    break

            # if cur_pos < len(itemList):
            #
            #     self.updateSupport(dscnt_node, itemList, cur_pos+1)

    # def traverse_trie(self, cur_node, cur_itms):
    #     if cur_node.label is not None:
    #         cur_itms.append(cur_node.label)
    #     if cur_node.marker == True:
    #         print(cur_itms, ': ', cur_node.support)
    #     for dscnt in cur_node.dscnts:
    #         self.traverse_trie(cur_node.dscnts[dscnt], copy.deepcopy(cur_itms))
    #     return

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
        while pos < len(cur_set):
            if cur_set[pos] not in cur_node.dscnts:
                return False
            cur_node = cur_node.dscnts[cur_set[pos]]
            pos += 1

        return True
        # if pos >= len(cur_set):
        #     return True
        # if cur_set[pos] not in cur_node.dscnts:
        #     return False
        # return self.checking_subpatterns(cur_node.dscnts[cur_set[pos]], cur_set, pos+1)

    def apriori_pruning(self):
        for i in range(0, len(self.cur_local_pattern)):
            tmp_cur = copy.deepcopy(self.cur_local_pattern)
            del tmp_cur[i]
            ret = self.checking_subpatterns(self.root_node, tmp_cur, 0)
            if ret is False:
                return False
        return True

    def frequent_set_generation(self, cur_node, cur_lvl):
        tmp_dscnts = copy.deepcopy(cur_node.dscnts)
        cur_node.dscnts = dict()
        if (cur_node.label is not None) and (cur_node.support >= self.threshold) and (cur_lvl == self.cur_level):
            self.pattern_count += 1
            cur_node.marker = True
        child_no = 0
        cur_node.support = 0
        for dscnt in tmp_dscnts:
            ret = self.frequent_set_generation(tmp_dscnts[dscnt], cur_lvl + 1)
            if ret > 0:
                child_no += ret
                cur_node.dscnts[dscnt] = tmp_dscnts[dscnt]
                cur_node.dscnts[dscnt].marker = False
        return child_no + cur_node.marker

    def print_FS(self, cur_node, cur_set):
        if cur_node.label is not None:
            cur_set.append(cur_node.label)
            if len(cur_set) == self.cur_level:
                print(cur_set, " : ", cur_node.support)
                return 1
        cnt = 0
        for dscnt in cur_node.dscnts:
            cnt += self.print_FS(cur_node.dscnts[dscnt], copy.deepcopy(cur_set))
        return cnt

    # def joining(self, cur_node, cur_set, depth):
    #     if cur_node.label is not None:
    #         cur_set.append(cur_node.label)
    #     if depth == self.cur_level - 1:
    #         itms = list(cur_node.dscnts.keys())
    #         # print(itms)
    #         itms.sort()
    #         # print(itms)
    #         for i in range(0, len(itms)):
    #             for j in range(i+1, len(itms)):
    #                 self.local_set.append(cur_set+[itms[i], itms[j]])
    #         return
    #     for dscnt in cur_node.dscnts:
    #         tmp_cur_set = copy.deepcopy(cur_set)
    #         self.joining(cur_node.dscnts[dscnt], tmp_cur_set, depth+1)

    def joining(self, cur_node, cur_set, depth):
        cur_node.marker = False
        if cur_node.label is not None:
            cur_set.append(cur_node.label)
        if depth == self.cur_level - 1:
            itms = list(cur_node.dscnts.keys())
            # print(itms)
            itms.sort()
            # print(itms)
            for i in range(0, len(itms)):
                for j in range(i+1, len(itms)):
                    self.joining_count += 1
                    self.cur_local_pattern = cur_set+[itms[i], itms[j]]
                    # print(self.cur_local_pattern, 'cur_local_pattern')
                    yes = self.apriori_pruning()
                    if yes == True:
                        self.candidate_count += 1
                        self.add_dscnt(cur_node.dscnts[itms[i]], itms[j])
                    # self.local_set.append(cur_set+[itms[i], itms[j]])
            return
        for dscnt in cur_node.dscnts:
            tmp_cur_set = copy.deepcopy(cur_set)
            self.joining(cur_node.dscnts[dscnt], tmp_cur_set, depth+1)

    def add_dscnt(self, cur_node, dscnt_lbl):
        cur_node.marker = False
        dscnt_node = Node()
        dscnt_node.label = dscnt_lbl
        cur_node.dscnts[dscnt_lbl] = dscnt_node
        return

    def after_joining_deletion(self, cur_node, cur_lvl):
        if cur_node.marker is True:
            print(cur_node.label, cur_node.marker)
        tmp_dscnts = copy.deepcopy(cur_node.dscnts)
        cur_node.dscnts = dict()
        if (cur_node.label is not None) and (cur_lvl == self.cur_level+1):
            # self.cur_level_joining_candidate_nodes.append(cur_node)
            self.pattern_count += 1
            cur_node.marker = True
        child_no = 0
        cur_node.support = 0
        for dscnt in tmp_dscnts:
            ret = self.after_joining_deletion(tmp_dscnts[dscnt], cur_lvl + 1)
            if ret > 0:
                child_no += ret
                cur_node.dscnts[dscnt] = tmp_dscnts[dscnt]
        return child_no + cur_node.marker

    def trie_traversal(self, cur_node, itms):
        if cur_node.label is not None:
            itms.append(cur_node.label)
        print(itms)
        for dscnt in cur_node.dscnts:
            self.trie_traversal(cur_node.dscnts[dscnt], copy.deepcopy(itms))


class Node():

    def __init__(self):
        self.label = None
        self.support = 0
        self.dscnts = dict()
        self.marker = False
        self.depth = None
