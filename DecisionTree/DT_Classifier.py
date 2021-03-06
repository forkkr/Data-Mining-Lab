import copy
import math


class DecisionTreeClassifier():

    def __init__(self, dtst, atrr_file, reverse_order, true_class, pruning_threshold):
        self.dataset_file = open(dtst, 'r')
        self.attr_file = open(atrr_file, 'r')
        self.attribute_typ_dict = dict()
        self.attribute_val_dict = dict()
        self.init_dataset = list()
        self.attribute_label = list()
        self.current_partition = list()
        self.cur_attr_lbl = list()
        self.root_node = None
        self.reverse_order = reverse_order
        self.true_class = true_class
        self.pruning_threshold = pruning_threshold
        # print(reverse_order, ' : order')
        return

    def preprocess(self):
        for attr_info in self.attr_file:
            attr_info.replace('\n', '')
            attr_info = attr_info.split(' ')
            # print(attr_info)
            self.attribute_label.append(str(attr_info[0]))
            if self.reverse_order == 1:
                self.attribute_label.reverse()
            self.attribute_typ_dict[str(attr_info[0])] = int(attr_info[1])
            # where 0 indicates discrete and 1 for continuous valued attribute

        for tuple_info in self.dataset_file:
            # print(tuple_info)
            tuple_info = tuple_info.replace('\n', '').replace('\r', '')
            tuple_info = tuple_info.split(',')
            # print(tuple_info, ' after splitting')

            if (len(tuple_info) == len(self.attribute_label)) and ('?' not in tuple_info):
                if self.reverse_order == 1:
                    tuple_info.reverse()
                self.init_dataset.append(copy.deepcopy(tuple_info))
                for i in range(0, len(self.attribute_label)):
                    if self.attribute_label[i] not in self.attribute_val_dict:
                        self.attribute_val_dict[self.attribute_label[i]] = []
                    if tuple_info[i] not in self.attribute_val_dict[self.attribute_label[i]]:
                        self.attribute_val_dict[self.attribute_label[i]].append(tuple_info[i])

        # print(self.init_dataset, ' dataset')
        # print(self.attribute_label)
        # print(self.attribute_typ_dict)
        # print(self.attribute_val_dict)
        return

    def induction(self):
        self.preprocess()
        self.current_partition = copy.deepcopy(self.init_dataset)
        self.cur_attr_lbl = copy.deepcopy(self.attribute_label)
        self.root_node = Node(None, None, False, None)
        # (self, attr_typ, attr, lf_mkr, cl_lbl):
        # print(self.current_partition)
        # print(self.cur_attr_lbl, ' Printing at induction')

        self.tree_build(self.root_node)

        # print(' Decision Tree: ')
        # self.traverse_decision_tree(self.root_node)
        return

    def tree_build(self, cur_node):

        tmp_cur_partition = copy.deepcopy(self.current_partition)
        tmp_cur_attr_lbl = copy.deepcopy(self.cur_attr_lbl)

        ret_val = self.base_case_checking()

        # where 0 for same class, 1 for empty attribute list and -1 for other cases

        if ret_val == 0:
            cur_node.leaf_marker = True
            cur_node.class_label, cur_node.instance_count = self.get_class()
            return

        elif ret_val == 1:
            # print('major voting code at here tree build')
            cur_node.leaf_marker = True
            cur_node.class_label, cur_node.instance_count, mx = self.major_voting()
            return


        selected_attr, attr_type, splitting_point, entropy = self.attribute_selection()
        # print(entropy, ' for attribute, ', selected_attr, tmp_cur_attr_lbl[selected_attr], splitting_point)

        if attr_type == 1:
            cur_node.attribute_type = 1
            cur_node.attribute = tmp_cur_attr_lbl[selected_attr]
            cur_node.splitting_point = splitting_point

            self.current_partition = copy.deepcopy(tmp_cur_partition)
            partition_dic = self.dataset_partition_for_continuous(selected_attr, splitting_point)
            # print(len(partition_dic[0]), len(partition_dic[1]), ' Partition Length')

            # self.current_partition = copy.deepcopy(tmp_cur_partition)
            self.cur_attr_lbl = copy.deepcopy(tmp_cur_attr_lbl)

            self.current_partition = self.get_partition(partition_dic[0], selected_attr)
            self.cur_attr_lbl.pop(selected_attr)

            if len(self.current_partition) <= self.pruning_threshold:
                self.current_partition = copy.deepcopy(tmp_cur_partition)  # major voting in parent's partition
                major, tot, mx = self.major_voting()
                new_node = Node(None, None, True, major)
                cur_node.descendents['<='] = new_node
                new_node.instance_count = max(mx, 0.0000001)
                cur_node.instance_count += mx
            else:
                new_node = Node(None, None, False, None)
                cur_node.descendents['<='] = new_node
                self.tree_build(new_node)
                cur_node.instance_count += cur_node.descendents['<='].instance_count

            self.current_partition = copy.deepcopy(tmp_cur_partition)
            self.cur_attr_lbl = copy.deepcopy(tmp_cur_attr_lbl)

            self.current_partition = self.get_partition(partition_dic[1], selected_attr)
            self.cur_attr_lbl.pop(selected_attr)

            if len(self.current_partition) <= self.pruning_threshold:
                self.current_partition = copy.deepcopy(tmp_cur_partition)  # major voting in parent's partition
                major, tot, mx = self.major_voting()
                new_node = Node(None, None, True, major)
                cur_node.descendents['>'] = new_node
                new_node.instance_count = max(mx, 0.0000001)
                cur_node.instance_count += mx
            else:
                new_node = Node(None, None, False, None)
                cur_node.descendents['>'] = new_node
                self.tree_build(new_node)
                cur_node.instance_count += cur_node.descendents['>'].instance_count

        else:
            cur_node.attribute_type = 0
            cur_node.attribute = tmp_cur_attr_lbl[selected_attr]

            partition_dic = self.dataset_partition_for_discrete(selected_attr)

            for attr_val in self.attribute_val_dict[tmp_cur_attr_lbl[selected_attr]]:
                self.current_partition = copy.deepcopy(tmp_cur_partition)
                self.cur_attr_lbl = copy.deepcopy(tmp_cur_attr_lbl)
                if attr_val not in partition_dic:
                    self.current_partition = dict()
                else:
                    self.current_partition = self.get_partition(partition_dic[attr_val], selected_attr)

                self.cur_attr_lbl.pop(selected_attr)

                if len(self.current_partition) <= self.pruning_threshold:
                    self.current_partition = tmp_cur_partition  # major voting in parent's partition
                    major, tot, mx = self.major_voting()
                    new_node = Node(None, None, True, major)
                    cur_node.descendents[attr_val] = new_node
                    new_node.instance_count = max(mx, 0.0000001)
                    cur_node.instance_count += mx
                else:
                    new_node = Node(None, None, False, None)
                    cur_node.descendents[attr_val] = new_node
                    self.tree_build(new_node)
                    cur_node.instance_count += cur_node.descendents[attr_val].instance_count

        # self.traverse_decision_tree(self.root_node)
        return

    def get_partition(self, lst, idx):
        partition = list()
        for id in lst:
            tmp_part = copy.deepcopy(self.current_partition[id])
            tmp_part.pop(idx)
            partition.append(copy.deepcopy(tmp_part))
        return partition

    def attribute_selection(self):
        init_gain = self.gain_info_for_initial()
        mx_attr = 0
        mx_type = 0
        mx_splitting_point = None
        mx = 0.0

        # print(self.cur_attr_lbl)
        for i in range(0, len(self.cur_attr_lbl)-1):
            attr = self.cur_attr_lbl[i]
            if self.attribute_typ_dict[attr] == 1:
                ret_gain, splitting_point = self.gain_info_calculation_for_continuous(i)
                ret_gain = init_gain - ret_gain
                # print(ret_gain, ' information gain ')

                if ret_gain > mx:
                    mx = ret_gain
                    mx_attr = i
                    mx_type = 1
                    mx_splitting_point = splitting_point
            else:
                ret_gain = self.gain_info_calculation_for_discrete(i)
                # print(ret_gain, init_gain, ' both gain at build')
                ret_gain = init_gain - ret_gain
                if ret_gain > mx:
                    # print(ret_gain, ' gain for ', i)
                    mx = ret_gain
                    mx_attr = i
                    mx_type = 0
        return mx_attr, mx_type, mx_splitting_point, mx

    def dataset_partition_for_continuous(self, idx, splt_point):
        partition_dic = dict()
        partition_dic[0] = []
        partition_dic[1] = []
        for i in range(0, len(self.current_partition)):
            val = float(self.current_partition[i][idx])
            if val <= splt_point:
                partition_dic[0].append(i)
            else:
                partition_dic[1].append(i)
        # print(partition_dic)
        return partition_dic

    def dataset_partition_for_discrete(self, idx):
        partition_dic = dict()
        for i in range(0, len(self.current_partition)):
            val = self.current_partition[i][idx]
            if val not in partition_dic:
                partition_dic[val] = [i]
            else:
                partition_dic[val].append(i)
        # print(partition_dic)
        return partition_dic

    def gain_info_calculation_for_discrete(self, idx):
        cnt_dict = dict()
        cnt_dic_dic = dict()
        for tuple in self.current_partition:
            cls = tuple[idx]
            if cls not in cnt_dict:
                cnt_dict[cls] = 1
            else:
                cnt_dict[cls] += 1

            if cls not in cnt_dic_dic:
                cnt_dic_dic[cls] = dict()
            if tuple[len(tuple)-1] not in cnt_dic_dic[cls]:
                cnt_dic_dic[cls][tuple[len(tuple)-1]] = 1
            else:
                cnt_dic_dic[cls][tuple[len(tuple) - 1]] += 1

        cnt = list(cnt_dict.values())
        total = len(self.current_partition)
        # print(cnt, total, ' at gain info ')
        sum = 0.0
        for attr_val in cnt_dict:
            demo = cnt_dict[attr_val]
            ratio = (demo/total)
            tmp_class_dic = cnt_dic_dic[attr_val]
            tmp_attr_sum = 0.0
            for val in tmp_class_dic:
                tmp_attr_sum += (-1)*(tmp_class_dic[val]/demo)*math.log2(tmp_class_dic[val]/demo)
            sum += ratio*tmp_attr_sum
        return sum

    def gain_info_calculation_for_continuous(self, idx):

        vals = self.attribute_val_dict[self.cur_attr_lbl[idx]]
        vals = [float(vals[i]) for i in range(0, len(vals))]
        vals.sort()
        # print(vals, ' sorted va/ls')
        split_points = [(vals[i]+vals[i+1])/2.0 for i in range(0, len(vals)-1)]
        cnt_dict = dict()
        cnt_dic_dic = dict()

        for tuple in self.current_partition:
            # print(tuple, idx, ' printing tuple with idx')
            cur_val = float(tuple[idx])
            for point in split_points:
                if str(point) not in cnt_dict:
                    cnt_dict[str(point)] = [0, 0]
                if str(point) not in cnt_dic_dic:
                    cnt_dic_dic[str(point)] = dict()
                    cnt_dic_dic[str(point)][0] = dict()
                    cnt_dic_dic[str(point)][1] = dict()

                if cur_val <= point:
                    cnt_dict[str(point)][0] += 1
                    if tuple[len(tuple) - 1] not in cnt_dic_dic[str(point)][0]:
                        cnt_dic_dic[str(point)][0][tuple[len(tuple) - 1]] = 1
                    else:
                        cnt_dic_dic[str(point)][0][tuple[len(tuple) - 1]] += 1
                else:
                    cnt_dict[str(point)][1] += 1
                    if tuple[len(tuple) - 1] not in cnt_dic_dic[str(point)][1]:
                        cnt_dic_dic[str(point)][1][tuple[len(tuple) - 1]] = 1
                    else:
                        cnt_dic_dic[str(point)][1][tuple[len(tuple) - 1]] += 1

        total = len(self.current_partition)
        mx = float('inf')
        selected_point = None

        for point in split_points:
            lst = cnt_dict[str(point)]
            # sum = (lst[0] / total)*((-1)*) * math.log2(lst[0] / total) +\
            #       (-1.0) * (lst[1] / total) * math.log2(lst[1] / total)

            sum = 0

            ratio0 = (lst[0] / total)
            ratio1 = (lst[1] / total)

            tmp_class_dic0 = cnt_dic_dic[str(point)][0]
            tmp_class_dic1 = cnt_dic_dic[str(point)][1]

            tmp_attr_sum = 0.0
            for val in tmp_class_dic0:
                tmp_attr_sum += (-1) * (tmp_class_dic0[val] / lst[0]) * math.log2(tmp_class_dic0[val] / lst[0])
            sum += ratio0 * tmp_attr_sum

            tmp_attr_sum = 0.0
            for val in tmp_class_dic1:
                tmp_attr_sum += (-1) * (tmp_class_dic1[val] / lst[1]) * math.log2(tmp_class_dic1[val] / lst[1])
            sum += ratio1 * tmp_attr_sum

            if sum < mx:
                mx = sum
                selected_point = point

        return mx, selected_point

    def gain_info_for_initial(self):
        cnt_dict = dict()
        total = 0
        for tuple in self.current_partition:
            cls = tuple[len(tuple)-1]
            total += 1
            if cls not in cnt_dict:
                cnt_dict[cls] = 1
            else:
                cnt_dict[cls] += 1
        cnt = list(cnt_dict.values())
        # total = len(self.current_partition)
        sum = 0.0
        for val in cnt:
            sum += (-1.0)*(val/total) * math.log2(val/total)
        return sum

    def major_voting(self):
        cnt_class = dict()
        mx = (-1)*float('inf')
        major = None
        for tuple in self.current_partition:
            cls = tuple[len(tuple)-1]
            if cls not in cnt_class:
                cnt_class[cls] = 1
            else:
                cnt_class[cls] += 1
            if cnt_class[cls] > mx:
                mx = cnt_class[cls]
                major = cls
        return major, int(len(self.current_partition)), mx

    def get_class(self):
        for tuple in self.current_partition:
            cls = tuple[len(tuple)-1]
            return cls, int(len(self.current_partition))

    def base_case_checking(self):
        # if len(self.cur_attr_lbl) == 1:
        #     return 1
        class_lst = list()
        for tuple in self.current_partition:
            if tuple[len(tuple)-1] not in class_lst:
                class_lst.append(tuple[len(tuple)-1])
            # if len(class_lst) >= 2:
            #     return -1
        if len(class_lst) == 1:
            return 0
        if len(self.cur_attr_lbl) == 1:
            return 1

        return -1

    def traverse_decision_tree(self, cur_node):
        print(cur_node.attribute_type)
        print(cur_node.attribute)
        if cur_node.attribute_type == 1:
            print('splitting point: ', cur_node.splitting_point)
        print(cur_node.leaf_marker)
        print(cur_node.class_label)
        print('\\ end Node')

        for dscnt in cur_node.descendents:
            print('Edge Label: ', dscnt)
            self.traverse_decision_tree(cur_node.descendents[dscnt])
        return

    def classifier(self, tst_fle):
        self.test_file = open(tst_fle, 'r')
        prediction_dic = dict()
        total_TP = 0
        total_cases =0
        # print('Test tuple: ')

        if self.true_class not in prediction_dic:
            prediction_dic[self.true_class] = dict()
            prediction_dic[self.true_class]['TP'] = 0
            prediction_dic[self.true_class]['FP'] = 0
            prediction_dic[self.true_class]['FN'] = 0
            prediction_dic[self.true_class]['P'] = 0

        for tuple_info in self.test_file:
            # print(tuple_info)

            tuple_info = tuple_info.replace('\n', '').replace('\r', '')
            tuple_info = tuple_info.split(',')
            # print(tuple_info, len(tuple_info))
            if len(tuple_info) == 0 or ('?' in tuple_info) or (len(tuple_info) < len(self.attribute_label)):
                # print(tuple_info)
                continue
            total_cases += 1
            if self.reverse_order == 1:
                tuple_info.reverse()
            # print('current tuple: ', tuple_info)
            found_class = self.find_class_for_tuple(self.root_node, tuple_info)
            # print(found_class, ' vs ', tuple_info[len(tuple_info)-1])

            if found_class not in prediction_dic:
                prediction_dic[found_class] = dict()
                prediction_dic[found_class]['TP'] = 0
                prediction_dic[found_class]['FP'] = 0
                prediction_dic[found_class]['FN'] = 0
                prediction_dic[found_class]['P'] = 0

            if tuple_info[len(tuple_info)-1] not in prediction_dic:
                prediction_dic[tuple_info[len(tuple_info)-1]] = dict()
                prediction_dic[tuple_info[len(tuple_info) - 1]]['TP'] = 0
                prediction_dic[tuple_info[len(tuple_info) - 1]]['FP'] = 0
                prediction_dic[tuple_info[len(tuple_info) - 1]]['FN'] = 0
                prediction_dic[tuple_info[len(tuple_info) - 1]]['P'] = 0

            prediction_dic[tuple_info[len(tuple_info) - 1]]['P'] += 1
            if found_class == tuple_info[len(tuple_info)-1]:
                total_TP += 1
                prediction_dic[found_class]['TP'] += 1

            elif found_class != tuple_info[len(tuple_info)-1]:
                prediction_dic[found_class]['FP'] += 1
                prediction_dic[tuple_info[len(tuple_info)-1]]['FN'] += 1
                # print(found_class, " Predicted vs Actual ", tuple_info[len(tuple_info)-1])

        return total_cases, total_TP, prediction_dic[self.true_class]['P'], prediction_dic[self.true_class]['TP'], prediction_dic[self.true_class]['FP']
        # print('Accuracy of this model: ', round(self.calculate_accuracy(total_cases, total_TP), 4))

    def find_class_for_tuple(self, cur_node, gvn_tpl):

        if cur_node.leaf_marker == True:
            return cur_node.class_label
        indx = self.attribute_label.index(cur_node.attribute)
        # print(gvn_tpl, len(gvn_tpl), cur_node.attribute, indx)
        val_key = gvn_tpl[indx]
        # print((type(val_key) != float), ' just to know')
        if int(self.attribute_typ_dict[cur_node.attribute]) == 1:
            if '?' == val_key:
                return self.find_class_for_missing_value_tuple(cur_node, gvn_tpl, cur_node.instance_count)[0]
            val_key = float(val_key)
            if val_key <= float(cur_node.splitting_point):
                if '<=' not in cur_node.descendents:
                    return self.find_class_for_missing_value_tuple(cur_node, gvn_tpl, cur_node.instance_count)[0]
                return self.find_class_for_tuple(cur_node.descendents['<='], gvn_tpl)
            else:
                if '>' not in cur_node.descendents:
                    return self.find_class_for_missing_value_tuple(cur_node, gvn_tpl, cur_node.instance_count)[0]
                return self.find_class_for_tuple(cur_node.descendents['>'], gvn_tpl)

        else:
            # print(cur_node.descendents)

            if val_key not in cur_node.descendents:
                return self.find_class_for_missing_value_tuple(cur_node, gvn_tpl, cur_node.instance_count)[0]
            return self.find_class_for_tuple(cur_node.descendents[val_key], gvn_tpl)

    def find_class_for_missing_value_tuple(self, cur_node, gvn_tpl, pre_instance_count):
        # print('Calling missing value handling...')
        if cur_node.leaf_marker == True:
            return [cur_node.class_label, max(0.0000001, cur_node.instance_count/pre_instance_count)]

        indx = self.attribute_label.index(cur_node.attribute)
        val_key = gvn_tpl[indx]

        if int(self.attribute_typ_dict[cur_node.attribute]) == 1:
            if '?' == val_key:
                ret_tuple_1 = [-1, -1]
                ret_tuple_2 = [-1, -1]
                if '<=' in cur_node.descendents:
                    ret_tuple_1 = self.find_class_for_missing_value_tuple(cur_node.descendents['<='], gvn_tpl, cur_node.instance_count)
                if '>' in cur_node.descendents:
                    ret_tuple_2 = self.find_class_for_missing_value_tuple(cur_node.descendents['>'], gvn_tpl, cur_node.instance_count)
                if ret_tuple_1[1] > ret_tuple_2[1]:
                    ret_tuple_1[1] *= (max(cur_node.descendents['<='].instance_count, 0.000001)/ cur_node.instance_count)
                    return ret_tuple_1
                else:
                    ret_tuple_2[1] *= (max(cur_node.descendents['>'].instance_count, 0.000001) / cur_node.instance_count)
                    return ret_tuple_2
            val_key = float(val_key)
            if val_key <= cur_node.splitting_point:
                if '<=' not in cur_node.descendents:
                    return self.find_class_for_missing_value_tuple(cur_node, gvn_tpl, cur_node.instance_count)
                ret_tuple = self.find_class_for_missing_value_tuple(cur_node.descendents['<='], gvn_tpl, cur_node.instance_count)
                # ret_tuple[1] *= (max(cur_node.descendents['<='].instance_count, 0.000001)/ cur_node.instance_count)
                return ret_tuple
            else:
                if '>' not in cur_node.descendents:
                    return self.find_class_for_missing_value_tuple(cur_node, gvn_tpl, cur_node.instance_count)
                ret_tuple = self.find_class_for_missing_value_tuple(cur_node.descendents['>'], gvn_tpl, cur_node.instance_count)
                # ret_tuple *= (max(cur_node.descendents['>'].instance_count, 0.000001) / cur_node.instance_count)
                return ret_tuple
        else:
            if val_key not in cur_node.descendents:
                mx_tuple = ['', 0.0]
                for dscnt in cur_node.descendents:
                    ret_tuple = self.find_class_for_missing_value_tuple(cur_node.descendents[dscnt], gvn_tpl, cur_node.instance_count)
                    ret_tuple[1] *= (max(cur_node.descendents[dscnt].instance_count, 0.000001)/cur_node.instance_count)
                    if mx_tuple[1] < ret_tuple[1]:
                        mx_tuple = ret_tuple
                return mx_tuple
            else:
                mx_tuple = self.find_class_for_missing_value_tuple(cur_node.descendents[val_key], gvn_tpl, cur_node.instance_count)
                # mx_tuple[1] *= (max(cur_node.descendents[val_key].instance_count, 0.000001)/cur_node.instance_count)
                return mx_tuple

    def calculate_accuracy(self, tc, tp):
        print('Total test case: ', tc, ' Total TP: ', tp)
        return (tp/tc)*100.0

    def calculate_f_measure(self):
        """ No need to implement """
        return

    def post_pruning(self, threshold):
        """ will be implemented later """
        return



class Node():

    def __init__(self, attr_typ, attr, lf_mkr, cl_lbl):
        self.attribute_type = attr_typ
        self.attribute = attr
        self.leaf_marker = lf_mkr
        self.class_label = cl_lbl
        self.descendents = dict()
        self.splitting_point = 0.0
        self.instance_count = 0
        return
