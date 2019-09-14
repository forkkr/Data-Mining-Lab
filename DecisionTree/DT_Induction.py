import math


class DecisionTree(object):
    dataset = []
    db_size = 0
    infoD = 0.0
    attr_cnt = 0
    attr_labels = []
    attr_type = []  # 0 = discrete, 1 = continuous
    class_labels = []
    class_details = {}  # class label: corresponding tuple ids

    pruning_threshold = 0.0

    tree_root = None

    def __init__(self, inputFile):
        self.dataset, self.class_details = self.read_data(inputFile)
        self.attr_labels = ['age', 'income', 'student', 'credit_rating', 'buys_computer']
        # self.attr_labels = ['outlook', 'temp', 'humidity', 'windy', 'play_tennis']
        self.attr_type = [0, 0, 0, 0, 0]

        tuple_ids = [i for i in range(0, self.db_size)]
        self.infoD = self.info_D(tuple_ids)
        # print('t',tuple_ids)
        attr_ids = [i for i in range(0, len(self.attr_labels) - 1)]
        self.tree_root = self.build_tree(attr_ids, tuple_ids)

    def read_data(self, inputFile):
        d = list()
        classes = dict()
        # for tennis : outlook,temp,humidity,windy,play
        # for exams: EXAM1,EXAM2,EXAM3,FINAL

        with open(inputFile, 'r') as infile:
            index = 0
            for line in infile:
                line = line.replace('\n', '').replace('\r', '')
                vals = line.split(',')
                cls = vals[len(vals) - 1]
                cls_tuples = classes.get(cls)
                if cls_tuples is None:
                    cls_tuples = list()
                    self.class_labels.append(cls)
                cls_tuples.append(index)
                classes[cls] = cls_tuples
                d.append(vals)
                index += 1
                # print(line)
        # print(d)
        self.db_size = len(d)
        return d, classes

    def info_D(self, tuple_ids):

        class_tuples = dict()

        for t in tuple_ids:
            data = self.dataset[t]
            cls = data[len(data) - 1]
            ct = class_tuples.get(cls, [])
            if ct is None:
                ct = list()
            ct.append(id)
            class_tuples[cls] = ct

        clss = class_tuples.keys()

        info = 0.0
        for c in clss:
            pi = len(class_tuples[c]) / (len(tuple_ids) * 1.0)
            # print(c,':',len(class_tuples[c]),'/',self.db_size)
            info = info - pi * math.log2(pi)
        # print('info(D)', round(info, 4), 'bits')
        return info

    def select_attr(self, attr_ids, tuple_ids):

        # print('se',attr_ids,tuple_ids)

        value_dicts = {}  # vt

        for attr_id in attr_ids:
            ref_for_value_tuple_dict_of_attr = dict()
            # print(attr_id)
            value_dicts[attr_id] = ref_for_value_tuple_dict_of_attr

        for t in tuple_ids:
            data = self.dataset[t]

            for attr_id in attr_ids:
                value_tuples_dict = value_dicts[attr_id]  # value:[tuple_ids]
                v = data[attr_id]
                vt = value_tuples_dict.get(v)
                if vt is None:
                    vt = list()
                vt.append(t)
                value_tuples_dict[v] = vt

        # print(value_dicts)

        best_attr_id = 0
        minInfo = math.inf

        for attr_id in attr_ids:
            value_tuples_dict = value_dicts[attr_id]
            values = value_tuples_dict.keys()
            info_a_D = 0.0
            for v in values:
                # print(self.attr_labels[attr_id],v,value_tuples_dict[v])
                info_a_D += (len(value_tuples_dict[v]) * 1.0) / self.db_size * self.info_D(value_tuples_dict[v])
            if info_a_D < minInfo:
                best_attr_id = attr_id
                minInfo = info_a_D

            # print('___', self.attr_labels[attr_id], round(info_a_D, 4), 'bits', 'Gain',round(self.infoD-info_a_D,4))

        # print('Selected', self.attr_labels[best_attr_id])
        return best_attr_id, value_dicts[best_attr_id]

    def class_distribution(self, t_ids):
        class_dict = {}
        for t in t_ids:
            data = self.dataset[t]
            cls = data[len(data) - 1]
            cls_cnt = class_dict.get(cls, 0)
            class_dict[cls] = cls_cnt + 1

        maxProb = -1 * math.inf
        major_class = None
        for k in class_dict.keys():
            p = class_dict[k] * 1.0 / len(t_ids)
            if p > maxProb:
                maxProb = p
                major_class = k
        # print(major_class, maxProb)
        return major_class, maxProb

    def build_tree(self, attr_ids, tuple_ids):
        attrs = attr_ids[:]
        root = Node(None, tuple_ids, False)
        self._grow_tree(root, attrs)
        # for i in root.next_nodes:
        #     print(i,i.test_attr_id)
        return root

    def _grow_tree(self, current_node, attr_list):
        # majority class
        major_class, prob = self.class_distribution(current_node.tuple_ids)

        if len(attr_list) == 0 or prob >= 1.0:
            current_node.isLeaf = True
            # current_node.rule = 'IF ' + current_node.rule + ' THEN ' + major_class + ', ' + prob
            current_node.next_nodes = [major_class, prob]
            return major_class, prob

        attrs = list(attr_list)
        best_attr_id, value_tuples = self.select_attr(attrs, current_node.tuple_ids)
        current_node.test_attr_id = best_attr_id
        attrs.remove(best_attr_id)

        # print(self.attr_labels[best_attr_id])

        for value in value_tuples.keys():
            # create child
            node = Node(value, value_tuples[value], False)
            node.parent = current_node
            node.parent.next_nodes.append(node)
            node.parent.children[value] = node
            # if current_node.test_attr_id is not None:
            #     node.rule = current_node.rule + "," + self.attr_labels[current_node.test_attr_id] + "=" + value
            self._grow_tree(node, attrs)

    def print_all_path(self):
        start_node = self.tree_root

        self.path_util(start_node,'')
        pass

    def path_util(self,cur_node,attr_path):
        if cur_node.isLeaf:
            print(attr_path,'->',cur_node.next_nodes)
            # print(cur_node.next_nodes)
        else:
            all_vals = cur_node.children.keys()
            all_child = []
            for v in all_vals:
                all_child.append(cur_node.children[v])

            # all_child = cur_node.next_nodes
            for ch in all_child:
                # attr_path.append(self.attr_labels[cur_node.test_attr_id]+'='+ ch.par_att_val)
                self.path_util(ch,attr_path+self.attr_labels[cur_node.test_attr_id]+'='+ ch.par_att_val+' ')

    def classify(self,newTuple_csvfmt):
        line = newTuple_csvfmt.replace('\n', '').replace('\r', '')
        vals = line.split(',')
        # print(vals)
        self.find_class(self.tree_root,vals)

    def find_class(self,node,vals):
        if node.isLeaf:
            print(vals, 'CLASS: ', node.next_nodes[0])
            return node.next_nodes
        test_attr_id = node.test_attr_id
        test_val = vals[test_attr_id]

        # print(test_attr_id)
        next = list(node.next_nodes)
        for ch in next:
            if ch.par_att_val==test_val:
                self.find_class(ch,vals)


class Node(object):
    def __init__(self, par_att_val, my_tuple_ids, isLeaf):
        self.test_attr_id = 0
        self.par_att_val = par_att_val
        self.isLeaf = isLeaf
        self.tuple_ids = my_tuple_ids

        self.parent = None
        self.rule = None
        self.next_nodes = list()
        self.children = dict()


dt = DecisionTree('../DecisionTree/buys_comp.csv')
# dt = DecisionTree('../DecisionTree/tennis.csv')
dt.print_all_path()
dt.classify('youth,high,yes,fair')
