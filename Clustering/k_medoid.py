import copy
from random import randint


class Medoid():

    attr_labels = list()
    attr_type = dict()

    repr_id = dict()
    repr_cost = dict()

    repr_set = list()
    non_pr_set = list()

    objects = list()

    attr_file = None
    object_file = None

    k_value = None
    num_obj = None

    mx_hf = dict()
    mn_hf = dict()
    mf = dict()

    clusters = dict()

    class_label = dict()

    def __init__(self, kv, af, of, cf):


        self.attr_labels = list()
        self.attr_type = dict()

        self.repr_id = dict()
        self.repr_cost = dict()

        self.repr_set = list()
        self.non_pr_set = list()

        self.objects = list()

        self.attr_file = None
        self.object_file = None

        self.k_value = None
        self.num_obj = None

        self.mx_hf = dict()
        self.mn_hf = dict()
        self.mf = dict()

        self.clusters = dict()

        self.class_label = dict()

        self.k_value = kv
        # print(af, of)
        self.attr_file = open(af, 'r')
        self.object_file = open(of, 'r')
        self.class_file = open(cf, 'r')
        pass

    def process_data(self):
        id = 0
        for cls in self.class_file:
            self.class_label[id] = cls
            id += 1

        for tpl in self.attr_file:
            # print(tpl)
            attrs = tpl.split(' ')
            # print(attrs, ' AHHHH')
            self.attr_labels.append(attrs[0])
            self.attr_type[attrs[0]] = int(attrs[1])
        for tpl in self.object_file:
            obj = tpl.split(',')
            self.objects.append(obj)

        self.num_obj = len(self.objects)
        # print('Attribute list: ', self.attr_labels)
        # print('Attribute type:', self.attr_type)
        # print('Objects: ', self.objects)
        for i in range(0, len(self.attr_labels)):
            if self.attr_type[self.attr_labels[i]] == 0:
                mn = float('inf')
                mx = (-1)*float('inf')

                for tuple in self.objects:

                    if '?' not in tuple:
                        # print(len(tuple), tuple)
                        tuple[i] = float(tuple[i])
                        mn = min(mn, tuple[i])
                        mx = max(mx, tuple[i])
                self.mx_hf[self.attr_labels[i]] = mx
                self.mn_hf[self.attr_labels[i]] = mn

            elif self.attr_type[self.attr_labels[i]] == 2:
                mn = float('inf')
                mx = (-1) * float('inf')

                for tuple in self.objects:
                    if '?' not in tuple:
                        tuple[i] = float(tuple[i])
                        mn = min(mn, tuple[i])
                        mx = max(mx, tuple[i])
                self.mx_hf[self.attr_labels[i]] = 1
                self.mn_hf[self.attr_labels[i]] = (mn-1)/(mx-1)
                self.mf[self.attr_labels[i]] = mx

        pass

    def initialize(self):
        i = 0
        while i < self.k_value:
            id = randint(0, self.num_obj-1)
            if id not in self.repr_set:
                self.repr_set.append(id)
                i += 1
        for i in range(0, self.num_obj):
            if i not in self.repr_set:
                self.non_pr_set.append(i)
        # self.repr_set = [0, 7]
        # self.non_pr_set = [1, 2, 3, 4, 5, 6]
        pass

    def numeric_dissimilarity(self, xif, xjf, attr):
        xjf = float(xjf)
        xif = float(xif)

        return abs(xif-xjf) / (self.mx_hf[attr] - self.mn_hf[attr])

    def nominal_dissimilarity(self, xif, xjf):
        if xif == xjf:
            return 0
        else:
            return 1

    def ordinal_dissimilarity(self, rif, rjf, attr):
        rif = float(rif)
        rjf = float(rjf)
        return self.numeric_dissimilarity((rif-1)/(self.mf[attr] - 1), (rjf-1)/(self.mf[attr] - 1), attr)

    def find_dissimilarity(self, p, oi):
        p_tuple = self.objects[p]
        oi_tuple = self.objects[oi]

        sum = 0
        count = 0
        # print(self.attr_labels, ' Attribute label')
        for i in range(0, len(self.attr_labels)):
            # print(self.attr_type[self.attr_labels[i]])
            if self.attr_type[self.attr_labels[i]] == 0:
                if ('?' not in p_tuple) and ('?' not in oi_tuple):
                    sum += self.numeric_dissimilarity(p_tuple[i], oi_tuple[i], self.attr_labels[i])
                    # print(sum, ' partial')
                    count += 1
                # print('YES IT is printed.........')
            elif self.attr_type[self.attr_labels[i]] == 1:
                if ('?' not in p_tuple) and ('?' not in oi_tuple):
                    sum += self.nominal_dissimilarity(p_tuple[i], oi_tuple[i])
                    # print(sum, ' partial')
                    count += 1
            else:
                if ('?' not in p_tuple) and ('?' not in oi_tuple):
                    sum += self.ordinal_dissimilarity(p_tuple[i], oi_tuple[i], self.attr_labels[i])
                    # print(sum, ' partial')
                    count += 1
        if count == 0:
            # print(' COUNT printed..')
            return float('inf')
        return sum/count

    def assign(self):

        total_cost = 0
        for i in range(0, self.num_obj):

            if i in self.repr_set:
                self.repr_id[i] = i
                self.repr_cost[i] = 0
            else:
                mn_dis = float('inf')
                mn_id = -1
                for rep in self.repr_set:
                    ret_dis = self.find_dissimilarity(i, rep)
                    # print(ret_dis, i, rep, ' -> Dis')
                    if ret_dis < mn_dis:
                        mn_dis = ret_dis
                        mn_id = rep
                self.repr_id[i] = mn_id
                self.repr_cost[i] = mn_dis
                total_cost += mn_dis
        return total_cost

    # def re_assign(self):
    #     pass

    def swap(self, prev_cost):
        for i in range(0, len(self.non_pr_set)):
            for j in range(0, len(self.repr_set)):
                # print(self.repr_set, self.non_pr_set)
                # print(self.repr_id)
                cur_cost = 0
                cur_cost_dic = copy.deepcopy(self.repr_cost)
                cur_id_dic = copy.deepcopy(self.repr_id)

                for k in range(0, len(self.non_pr_set)):
                    # print(cur_cost, self.non_pr_set[k])
                    if self.non_pr_set[i] == self.non_pr_set[k]:
                        cur_id_dic[self.non_pr_set[i]] = self.non_pr_set[i]
                        cur_cost_dic[self.non_pr_set[i]] = 0

                    elif self.repr_id[self.non_pr_set[k]] == self.repr_set[j]:
                        # print(self.non_pr_set[k], ' vs ', self.repr_set[j], ' replaced by ' , self.non_pr_set[i])
                        mn_dis = self.find_dissimilarity(self.non_pr_set[k], self.non_pr_set[i])
                        mn_id = self.non_pr_set[i]
                        for rep in self.repr_set:
                            if rep == self.repr_set[j]:
                                continue
                            else:
                                ret_dis = self.find_dissimilarity(self.non_pr_set[k], rep)
                                if ret_dis < mn_dis:
                                    mn_dis = ret_dis
                                    mn_id = rep
                        cur_cost_dic[self.non_pr_set[k]] = mn_dis
                        cur_id_dic[self.non_pr_set[k]] = mn_id
                        cur_cost += mn_dis
                        # print('min cost: ', mn_dis)
                    else:
                        ret_dis = self.find_dissimilarity(self.non_pr_set[i], self.non_pr_set[k])
                        if ret_dis < cur_cost_dic[self.non_pr_set[k]]:
                            cur_cost_dic[self.non_pr_set[k]] = ret_dis
                            cur_id_dic[self.non_pr_set[k]] = self.non_pr_set[i]
                        cur_cost += cur_cost_dic[self.non_pr_set[k]]

                mn_dis = self.find_dissimilarity(self.repr_set[j], self.non_pr_set[i])
                mn_id = self.non_pr_set[i]
                for rep in self.repr_set:
                    if rep == self.repr_set[j]:
                        continue
                    else:
                        ret_dis = self.find_dissimilarity(self.repr_set[j], rep)
                        if ret_dis < mn_dis:
                            mn_dis = ret_dis
                            mn_id = rep
                cur_cost_dic[self.repr_set[j]] = mn_dis
                cur_id_dic[self.repr_set[j]] = mn_id
                cur_cost += mn_dis
                # print('New cost: ', cur_cost)

                if cur_cost < prev_cost:
                    prev_cost = cur_cost
                    tmp_x = self.repr_set[j]
                    self.repr_set[j] = self.non_pr_set[i]
                    self.non_pr_set[i] = tmp_x

                    self.repr_id = copy.deepcopy(cur_id_dic)
                    self.repr_cost = copy.deepcopy(cur_cost_dic)
                # print('current cost: ', prev_cost)
        return prev_cost

    def run_algorithm(self, yes_purity):
        self.process_data()
        self.initialize()
        cur_cost = self.assign()
        print(self.repr_id)
        # print('Total Cost: ', cur_cost)
        prev_cost = cur_cost+111111111111
        prev_set = []
        # print('Before swapping: ', self.repr_set, self.non_pr_set)
        while prev_set != self.repr_set:
            prev_cost = copy.deepcopy(cur_cost)
            prev_set = copy.deepcopy(self.repr_set)
            cur_cost = self.swap(cur_cost)
            print(prev_set, self.repr_set)

        # print('After swapping: ', self.repr_set, self.non_pr_set)
        # print(self.repr_id)
        # print('Total Cost: ', cur_cost)
        for cr in self.repr_set:
            self.clusters[cr] = []
            self.clusters[cr].append(cr)
        for ncr in self.non_pr_set:
            self.clusters[self.repr_id[ncr]].append(ncr)
        for clky in self.clusters:
            print(clky, ':', len(self.clusters[clky]))
        s_co = self.silhouette_coefficient()
        sum_s_co = 0
        cls_total = 0
        for clky in s_co:
            sum_s_co += s_co[clky]
            cls_total += len(self.clusters[clky])
            # print(s_co[clky], ' for ', clky)

        sum_dun_co = 0
        dun_total = 0
        dun_co = self.dunn_index()
        for id in dun_co:
            sum_dun_co += dun_co[id]
        dun_total = len(dun_co)
        if yes_purity:
            return sum_s_co/cls_total, sum_dun_co/dun_total, self.determine_purity()
        else:
            return sum_s_co / cls_total, sum_dun_co / dun_total

    def silhouette_coefficient(self):
        a_value = dict()
        b_value = dict()
        s_value = dict()
        for clky in self.clusters:
            a_value[clky] = 5050
            b_value[clky] = 5050
            s_value[clky] = 0
            for val_i in self.clusters[clky]:
                ind_a = 0.0
                for val_j in self.clusters[clky]:
                    ind_a += self.find_dissimilarity(val_i, val_j)

                ind_a /= (len(self.clusters[clky])-1)

                ind_b = float('inf')
                for not_clky in self.clusters:
                    if clky != not_clky:
                        tmp_b = 0
                        for val_k in self.clusters[not_clky]:
                            tmp_b += self.find_dissimilarity(val_i, val_k)
                        tmp_b /= len(self.clusters[not_clky])
                        ind_b = min(ind_b, tmp_b)

            #     b_value[clky] += ind_b
            #     a_value[clky] += ind_a
            # b_value[clky] /= len(self.clusters[clky])
            # a_value[clky] /= (len(self.clusters[clky])-1)
            #     if (ind_b - ind_a)/(max(ind_b, ind_a)) < 0:
            #         print(ind_a, ind_b)
                s_value[clky] += (ind_b - ind_a)/(max(ind_b, ind_a))
            # s_value[clky] /= (len(self.clusters[clky]))

        # print(b_value, a_value, s_value)
        return s_value

    def dunn_index(self):
        dunn_value = dict()
        for clky in self.clusters:
            diameter = float('-inf')
            separation = float('inf')
            for ai in self.clusters[clky]:
                for bi in self.clusters[clky]:
                    diameter = max(self.find_dissimilarity(ai, bi), diameter)
                for nonclky in self.clusters:
                    if nonclky != clky:
                        for ci in self.clusters[nonclky]:
                            separation = min(self.find_dissimilarity(ai, ci), separation)
            dunn_value[clky] = separation/diameter
        return dunn_value

    def determine_purity(self):
        purity_val = 0

        total_instance = 0

        for clky in self.clusters:
            tmp_dic = dict()
            total_instance += len(self.clusters[clky])
            for val_i in self.clusters[clky]:
                if self.class_label[val_i] not in tmp_dic:
                    tmp_dic[self.class_label[val_i]] = 0
                tmp_dic[self.class_label[val_i]] += 1
            mx_val = 0
            for cls in tmp_dic:
                mx_val = max(mx_val, tmp_dic[cls])

            purity_val += mx_val
        return purity_val/total_instance