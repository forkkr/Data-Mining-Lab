import copy
import itertools

from FP_Growth.DataSet import DatasetProcessing


class FPGrowth():
    threshold = None
    fre_itms = dict()
    root_node = None
    prev_link = dict()
    init_header = dict()
    intermediate_header = dict()
    inter_fre_itms = dict()
    conditional_fre_itms = dict()
    conditional_base = []

    def __init__(self, thld):
        self.threshold = thld*len(DatasetProcessing.db)
        pass

    def fp_growth(self):
        self.find_frequent_itms()
        self.root_node = TreeNode()
        flag = 0
        self.prev_link = dict()
        self.init_header = dict()
        for itms in DatasetProcessing.db:
            self.build_fp_tree(self.root_node, itms, flag, 1)
            flag %= 2
            flag += 1
        tmp_list = []

        # self.print_fp_tree(self.root_node, [])

        for itm in sorted(self.fre_itms, key = self.fre_itms.get, reverse=True):
            if self.fre_itms[itm] >= self.threshold:
                tmp_list.append(itm)
        self.fre_itms = tmp_list
        self.fre_itms.reverse()
        print(self.fre_itms, ' Frequent items at fp_growth')
        # print(self.init_header, ' Initial Header at fp_growth')
        num_of_patterns, num_of_conditional_tree = self.projection_and_generation()
        print('Total Patterns: ', len(num_of_patterns))
        print('Total conditional tree: ', num_of_conditional_tree)
        return

    def print_fp_tree(self, cur_node, cur_itms):
        if cur_node.label is not None:
            cur_itms.append(cur_node.label)
        print(cur_itms)
        for dscnt in cur_node.dscnts:
            self.print_fp_tree(cur_node.dscnts[dscnt], copy.deepcopy(cur_itms))
        return

    def traverse_same_itm_link(self, cur_node):
        tmp = 0
        while cur_node is not None:
            tmp += 1
            cur_node = cur_node.node_link
        return tmp

    def find_frequent_itms(self):
        for itms in DatasetProcessing.db:
            for itm in itms:
                if int(itm) not in self.fre_itms:
                    self.fre_itms[int(itm)] = 1
                else:
                    self.fre_itms[int(itm)] += 1
        tmp_dp = []
        for itms in DatasetProcessing.db:
            tmp_itms = []
            for itm in itms:
                itm = int(itm)
                if self.fre_itms[itm] >= self.threshold:
                    tmp_itms.append((self.fre_itms[itm], itm))
            tmp_itms.sort()
            if len(tmp_itms):
                tmp_itms_cur = []
                for tmp_itm in tmp_itms:
                    tmp_itms_cur.append(tmp_itm[1])
                tmp_itms_cur.reverse()
                tmp_dp.append(tmp_itms_cur)
        DatasetProcessing.db = tmp_dp
        return

    def build_fp_tree(self, cur_node, itms, flag, support):
        if len(itms) == 0:
            return
        if itms[0] not in cur_node.dscnts:
            cur_node.dscnts[itms[0]] = TreeNode()
            cur_node.dscnts[itms[0]].parent_link = cur_node
            if itms[0] not in self.init_header:
                self.init_header[itms[0]] = cur_node.dscnts[itms[0]]
                self.prev_link[itms[0]] = cur_node.dscnts[itms[0]]
            else:
                self.prev_link[itms[0]].node_link = cur_node.dscnts[itms[0]]
                self.prev_link[itms[0]] = cur_node.dscnts[itms[0]]
        cur_node.dscnts[itms[0]].support += support
        cur_node.dscnts[itms[0]].label = itms[0]
        prev_itm = itms[0]
        itms.pop(0)
        self.build_fp_tree(cur_node.dscnts[prev_itm], itms, flag, support)
    pass


    def projection_and_generation(self):
        cur_fre_itms = copy.deepcopy(self.fre_itms)
        cur_header = self.init_header
        cur_root_node = self.root_node
        if cur_fre_itms == []:
            return [], -1
        for itm in cur_fre_itms:
            suffix_node = cur_header[itm]
            # print('Suffix node : ', itm)
            ret = self.traverse_same_itm_link(suffix_node)
            if ret == 1:
                num_itms = self.traverse_upward(suffix_node)
                patterns = self.pattern_generation_for_single_path(num_itms)
                return patterns, 0
            else:
                break

        total_patterns = []
        tot_conditional_fp_tree = 0

        for itm in cur_fre_itms:

            self.fre_itms = []
            suffix_node = cur_header[itm]
            self.root_node = TreeNode()
            self.init_header = dict()
            self.conditional_fre_itms = dict()
            self.projection_by_itm(suffix_node)
            for fre_itm in cur_fre_itms:
                if fre_itm not in self.conditional_fre_itms:
                    continue
                if fre_itm == itm:
                    continue

                if self.conditional_fre_itms[fre_itm] >= self.threshold:
                    self.fre_itms.append(fre_itm)
            flag = 0
            for itm_st, support in self.conditional_base:
                # print(itm_st, support, ' Pushing into FP tree')
                self.build_conditional_FP_tree(self.root_node, itm_st, flag, support)
                flag %= 2
                flag += 1

            # pattern_count = self.projection_and_generation()
            # pattern_count += 1
            # self.traverse_conditional_FP_tree(self.root_node, [])
            pattern_count, cnd_fp_tree = self.projection_and_generation()
            pattern_count = self.pattern_generation_for_multi_path(pattern_count, itm)
            # print(' sub total: ', pattern_count, ' for ', itm)
            # total_count += pattern_count
            total_patterns += pattern_count
            # print(' sub total conditional tree : ', cnd_fp_tree+1, ' for ', itm)
            tot_conditional_fp_tree += cnd_fp_tree + 1
        return total_patterns, tot_conditional_fp_tree

    def projection_by_itm(self, cur_node):
        flag = 0
        self.conditional_base = []
        while cur_node is not None:
            get_itms = self.get_conditional_base(cur_node,cur_node.support)
            get_itms.pop()
            if len(get_itms):
                self.conditional_base.append((get_itms, cur_node.support))
                # self.build_conditional_base_trie(cur_node, get_itms, cur_node.support)
                # self.build_conditional_FP_tree(cur_trie_root, get_itms, flag, cur_node.support)
            cur_node = cur_node.node_link
            flag %= 2
            flag += 1

    def build_conditional_FP_tree(self, cur_node, itms, flag, support):
        if len(itms) == 0:
            return
        if itms[0] not in self.fre_itms:
            itms.pop(0)
            self.build_conditional_FP_tree(cur_node, itms, flag, support)
            return
        if itms[0] not in cur_node.dscnts:
            cur_node.dscnts[itms[0]] = TreeNode()
            cur_node.dscnts[itms[0]].label =  itms[0]
            cur_node.dscnts[itms[0]].parent_link = cur_node
            if itms[0] not in self.init_header:
                self.init_header[itms[0]] = cur_node.dscnts[itms[0]]
                self.prev_link[itms[0]] = cur_node.dscnts[itms[0]]
            else:
                self.prev_link[itms[0]].node_link = cur_node.dscnts[itms[0]]
                self.prev_link[itms[0]] = cur_node.dscnts[itms[0]]
        cur_node.dscnts[itms[0]].support += support
        # if itms[0] not in self.conditional_fre_itms:
        #     self.conditional_fre_itms[itms[0]] = support
        # else:
        #     self.conditional_fre_itms[itms[0]] += support
        prev_itm = itms[0]
        itms.pop(0)
        self.build_conditional_FP_tree(cur_node.dscnts[prev_itm], itms, flag, support)

    # def build_conditional_fp_trie(self, cur_node):
    #     # if cur_node is None:
    #     #     # print(" Cur_Node is None... ")
    #     if cur_node.node_link is None:
    #         ancstr = cur_node.parent_link
    #         # print(cur_node.label, ' at build conditional fp trie')
    #         del ancstr.dscnts[cur_node.label]
    #         return
    #     self.build_conditional_fp_trie(cur_node.node_link)
    #     return

    def traverse_conditional_FP_tree(self, cur_node, itmset):
        if len(cur_node.dscnts) == 0:
            print(itmset)
            return
        for dscnt in cur_node.dscnts:
            tmp_itmset = itmset
            tmp_itmset.append(cur_node.dscnts[dscnt].label)
            self.traverse_conditional_FP_tree(cur_node.dscnts[dscnt], tmp_itmset)

    def build_conditional_base_trie(self, cur_node, itms, support):
        if len(itms) == 0:
            return
        if itms[0] not in cur_node.dscnts:
            new_node = TreeNode()
            new_node.label = itms[0]
            cur_node.dscnts[itms[0]] = new_node
            new_node.parent_link = cur_node
        cur_node.dscnts[itms[0]] += support
        if itms[0] not in self.conditional_fre_itms:
            self.conditional_fre_itms[itms[0]] = support
        else:
            self.conditional_fre_itms[itms[0]] += support
        prev_itm = itms[0]
        itms.pop(0)
        self.build_conditional_base_trie(cur_node.dscnts[prev_itm], itms, support)
        return

    def count_conditional_fp_trie(self, cur_node, count):
        if cur_node.dscnts is None:
            return count+1

    def get_conditional_base(self, cur_node, support):
        if cur_node.label is None:
            return []
        ret = self.get_conditional_base(cur_node.parent_link, support)
        if cur_node.label not in self.conditional_fre_itms:
            self.conditional_fre_itms[cur_node.label] = support
        else:
            self.conditional_fre_itms[cur_node.label] += support
        ret.append(cur_node.label)
        return ret

    def traverse_upward(self, cur_node):
        tmp = []
        while cur_node.parent_link is not None:
            tmp.append(cur_node.label)
            cur_node = cur_node.parent_link
        tmp.reverse()

        # if cur_node.parent_link is None:
        #     return []
        # tmp = []
        # tmp.append(cur_node.label)
        # tmp += self.traverse_upward(cur_node.parent_link)
        return tmp

    def pattern_generation_for_single_path(self, itms):
        all_patterns = []
        tmp_itms = []
        for itm in itms:
            tmp_itms.append(int(itm))
        itms = tmp_itms
        for i in range(1 , len(itms)+1):
            get_pp = itertools.combinations(itms , r =i)
            tmp_list = []
            for pp in get_pp:
                pp = list(pp)
                tmp_list.append(pp)
            all_patterns += tmp_list
        return all_patterns

    def pattern_generation_for_multi_path(self, patterns, itm):
        for pp in patterns:
            pp.append(itm)
        tmp_list = []
        tmp_list.append(int(itm))
        patterns.append(tmp_list)
        return patterns

class TreeNode():

    def __init__(self):
        self.label = None
        self.support = 0
        self.node_link = None
        self.parent_link = None
        self.dscnts = dict()
        pass
