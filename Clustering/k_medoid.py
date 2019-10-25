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

    def __init__(self, kv, af, of):
        self.k_value = kv
        self.attr_file = open(af, 'r')
        self.object_file = open(of, 'r')
        pass

    def process_data(self):
        for tpl in self.attr_file:
            attrs = tpl.split(' ')
            self.attr_labels.append(attrs[0])
            self.attr_type[attrs[0]] = int(attrs[1])
        for tpl in self.object_file:
            obj = tpl.split(',')
            self.objects.append(obj)

        self.num_obj = len(self.objects)
        print('Attribute list: ', self.attr_labels)
        print('Attribute type:', self.attr_type)
        print('Objects: ', self.objects)
        for i in range(0, len(self.attr_labels)):
            if self.attr_type[self.attr_labels[i]] == 0:
                mn = float('inf')
                mx = (-1)*float('inf')

                for tuple in self.objects:
                    if '?' not in tuple:
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

        for i in range(0, len(self.attr_labels)):
            if self.attr_type[self.attr_labels[i]] == 0:
                if ('?' not in p_tuple) and ('?' not in oi_tuple):
                    sum += self.numeric_dissimilarity(p_tuple[i], oi_tuple[i], self.attr_labels[i])
                    # print(sum, ' partial')
                    count += 1
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

    def run_algorithm(self):
        self.process_data()
        self.initialize()
        cur_cost = self.assign()
        print(self.repr_id)
        print('Total Cost: ', cur_cost)
        prev_cost = cur_cost+111111111111
        print('Before swapping: ', self.repr_set, self.non_pr_set)
        while prev_cost > cur_cost:
            prev_cost = cur_cost
            cur_cost = self.swap(cur_cost)
        print('After swapping: ', self.repr_set, self.non_pr_set)
        print(self.repr_id)
        print('Total Cost: ', cur_cost)
        pass
