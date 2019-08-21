from FP_Growth.DataSet import DatasetProcessing

class FPGrowth():
    threshold = None
    fre_itms = dict()
    root_node = None
    prev_link = dict()
    init_header = dict()
    intermediate_header = dict()
    inter_fre_itms = dict()

    def __init__(self, thld):
        self.threshold = thld
        pass

    def fp_growth(self):
        self.find_frequent_itms()
        self.root_node = TreeNode()
        flag = 0
        for itms in DatasetProcessing.db:
            self.build_fp_tree(self.root_node, itms, flag)
            flag %= 2
            flag += 1
        num_of_patterns = 0
        for itm in sorted(self.fre_itms):
            prj_db = self.traverse_same_itm_link(self.init_header[itm])
            self.projection_and_generation(self.init_header[itm], prj_db)

    def traverse_same_itm_link(self, cur_node):
        tmp = 1
        if cur_node.node_link is None:
            return tmp
        # tmp.append(cur_node.support)
        tmp += self.traverse_same_itm_link(cur_node.node_link)
        return tmp

    def find_frequent_itms(self):
        for itms in DatasetProcessing.db:
            for itm in itms:
                if itm not in self.fre_itms:
                    self.fre_itms[itm] = 1
                else:
                    self.fre_itms[itm] += 1
        tmp_dp = []
        for itms in DatasetProcessing.db:
            tmp_itms = []
            for itm in itms:
                if self.fre_itms[itm] >= self.threshold:
                    tmp_itms.append((self.fre_itms[itm], itm))
            tmp_itms.sort()
            if len(tmp_itms):
                tmp_dp.append(tmp_itms)
        DatasetProcessing.db = tmp_dp
        return

    def build_fp_tree(self, cur_node, itms, flag):
        itms.pop(0)
        if len(itms) == 0:
            return
        if itms[0] not in cur_node.dscnts:
            cur_node.dscnts[itms[0]] = TreeNode()
            cur_node.dscnts[itms[0]].parent_link = cur_node
            if flag == 0:
                self.init_header[itms[0]] = cur_node.dscnts[itms[0]]
                self.prev_link[itms[0]] = cur_node.dscnts[itms[0]]
            else:
                self.prev_link[itms[0]].node_link = cur_node.dscnts[itms[0]]
                self.prev_link[itms[0]] = cur_node.dscnts[itms[0]]
        cur_node.dscnts[itms[0]].support += 1
        self.build_fp_tree(cur_node.dscnts[itms[0]], itms, flag)
    pass

    def projection_and_generation(self):
        cur_fre_itms = self.fre_itms
        cur_header = self.init_header
        for itm in sorted(cur_fre_itms):
            suffix_node = cur_header[itm]
            ret = self.traverse_same_itm_link(suffix_node)
            if ret == 1:
                num_itms = self.traverse_upward(suffix_node)
                return 2 ** num_itms - 1
            else:
                break
        for itm in sorted(cur_fre_itms):
            suffix_node = cur_header[itm]


        self.inter_fre_itms = dict()
        tmp_cur_node = cur_node
        for i in range(0, len(prj_db)):
            self.traverse_upward(tmp_cur_node, prj_db[i])
            tmp_cur_node = tmp_cur_node.node_link
        cur_fre_itms = dict()
        for itm in self.inter_fre_itms:
            if self.inter_fre_itms[itm] >= self.threshold:
                cur_fre_itms[itm] = self.inter_fre_itms[itm]
        cur
        pass

    def prejection_by_itm(self, cur_node, cur_trie_root):
        flag = 0
        while cur_node is not None:
            get_itms = self.get_conditional_base(cur_node)
            self.build_conditional_trie(cur_trie_root, get_itms, cur_node.support)

    def build_conditional_trie(self, cur_node, itms, cur_support):
        itms.pop(0)
        if len(itms) == 0:
            return
        if itms[0] not in cur_node.dscnts:
            new_node = TreeNode()
            new_node.label = itms[0]
            new_node.parent_link = cur_node
        cur_node.dscnts[itms[0]].support += cur_support


    def get_conditional_base(self, cur_node):
        if cur_node.label is None:
            return []
        ret = self.get_conditional_base(cur_node.parent_link)
        ret.append(cur_node.label)
        return ret

    def traverse_upward(self, cur_node):
        if cur_node.parent_link is None:
            return 0
        tmp = 1
        tmp += self.traverse_upward(cur_node.parent_link)
        return tmp


class TreeNode():

    def __init__(self):
        self.label = None
        self.support = 0
        self.node_link = None
        self.parent_link = None
        self.dscnts = dict()
        pass
