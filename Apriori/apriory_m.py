import copy,math,time,os,errno


def ffopen(fileLocation, mode, title=None):
    # if not os.path.exists(os.path.dirname(fileLocation)):
    if not os.path.exists(fileLocation):
        try:
            os.makedirs(os.path.dirname(fileLocation))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
        f = open(fileLocation, mode)
        if title is None:
            title = input('Creating New File, Enter Title: ')
        f.write(title)
        f.close()

    f = open(fileLocation, mode)
    return f


class MyApriory:

    db = []
    threshold = 1
    dataset_name = ''

    items = list()

    cand_count_after_join = list()
    cand_count_after_prune = list()
    count_freq_patterns = list()
    final_patterns = list() # L
    
    local_set = []
    candidates = []
    cur_level = 1

    time_required = 0.0
    
    trie_root = None

    def __init__(self, file=None,minsup=None, dataset_name = None):
        if file is None:
            file = input('File Path (full): ').strip()
        if minsup is None:
            minsup = float(input('Enter min_sup in % (float): ').strip())
        if dataset_name is None:
            dataset_name = input('Enter Dataset Name: ')
            self.dataset_name = dataset_name



        with open(file,'r') as f:
            for transaction in f:
                if transaction.strip()=='':
                    break
                items = transaction.strip().split()
                self.db.append(items)

        self.threshold = math.ceil(len(MyApriory.db) * minsup / 100.0)

        self.trie_root = None

        output_file = '../Files/'+dataset_name+'_apriori.csv'
        title = 'dataset,min_sup,total_candidates,total_patterns,time_required,memory_required\n'
        outf = ffopen(output_file,'a',title)
        result = self.run()
        print(result)
        result_s = list()
        for i in range(0,len(result)):
            result_s.append(str(result[i]))

        buffer = ','.join(result_s)
        buffer_s = dataset_name+','+str(minsup)+','+buffer+'\n'
        print('writing into file...')
        outf.write(buffer_s)
        outf.close()

    def run(self):

        t0 = time.time()

        L1 = self.find_L1()
        self.count_freq_patterns.append(len(L1))

        pfmt = '{0:5}  | {1:15} | {2:15} | {3:15}'
        print('_______', '_________________', '_________________', '_________________')
        print(pfmt.format('Level', 'After Joining', 'After Pruning', 'Frequent Patterns'))
        print('_______', '_________________', '_________________', '_________________')
        print(pfmt.format('L1', '--', '--', len(L1)))
        
        C2 = list()
        for i in range(0, len(L1)):
            for j in range(i + 1, len(L1)):
                C2.append([L1[i][0], L1[j][0]])
        
        self.cand_count_after_prune.append(len(C2))

        self.cur_level = 2
        C2.sort()
        self.candidates = C2
        self.trie_root = Node()
        for can in self.candidates:
            self.build_trie(self.trie_root, can, 0)

        for i in range(0, len(self.db)):
            self.support_update(self.trie_root, i)

        self.frequent_set_generation(self.trie_root)

        tot_fs = self.count_freq(self.trie_root, [])
        self.count_freq_patterns.append(tot_fs)

        print_buffer = ['L2', len(C2), len(C2)]
        print_buffer.append(tot_fs)
        print(pfmt.format(*print_buffer))
        
        while tot_fs>self.cur_level or len(self.candidates)>0:
            self.local_set = []
            self.joining(self.trie_root, [], 0)
            self.cand_count_after_join.append(self.local_set)

            self.candidate = []
            self.candidate_generation()
            self.cand_count_after_prune.append(len(self.candidate))

            self.cur_level += 1


            
            for can in self.candidate:
                # print(can)
                self.build_trie(self.trie_root, can, 0)

            for i in range(0, len(self.db)):
                self.support_update(self.trie_root, i)

            self.frequent_set_generation(self.trie_root)

            tot_fs = self.count_freq(self.trie_root, [])
            self.count_freq_patterns.append(tot_fs)

            print_buffer = []
            print_buffer.append('L' + str(self.cur_level))
            print_buffer.append(len(self.local_set))
            print_buffer.append(len(self.candidate))
            print_buffer.append(tot_fs)
            print(pfmt.format(*print_buffer))


            if tot_fs <= self.cur_level:
                print(tot_fs,'<= cur_level',self.cur_level)
                break

        t1 = time.time()

        print('_______', '_________________', '_________________', '_________________')

        print('Total Candidates Generated: ',sum(self.cand_count_after_prune))
        print('Total Patterns Found: ', sum(self.count_freq_patterns))
        print('Time Required: ',round(t1-t0,4))


        return [sum(self.cand_count_after_prune),sum(self.count_freq_patterns), round(t1-t0,4)]

    #########################

    def find_L1(self):
        itms_dic = dict()
        for itms in self.db:
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
        return L1
    
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
        if cur_set[pos] not in cur_node.children:
            return False
        return self.checking_subpatterns(cur_node.children[cur_set[pos]], cur_set, pos+1)

    def apriori_pruning(self):
        for i in range(0, len(self.cur_local_pattern)):
            tmp_cur = copy.deepcopy(self.cur_local_pattern)
            del tmp_cur[i]
            ret = self.checking_subpatterns(self.trie_root, tmp_cur, 0)
            if ret is False:
                return False
        return True
    
    def build_trie(self, cur_node, itemset, pos): #recursively adding a candidate into trie
        if pos >= len(itemset):
            return
        if itemset[pos] in cur_node.children:
            cur_node.children[itemset[pos]].support = 0
            self.build_trie(cur_node.children[itemset[pos]], itemset, pos+1)
        else:
            new_node = Node()
            cur_node.children[itemset[pos]] = new_node
            # print(candidate[pos], ' at build')
            new_node.label = itemset[pos]
            new_node.support = 0
            self.build_trie(new_node, itemset, pos+1)
        pass
    
    def support_update(self, cur_node, trn_id):
        # print(self.db[trn_id], type(cur_node.label))
        got = False
        if cur_node.label is not None:
            # print(cur_node.label, ' cur_node label at support_update')
            l = 0
            r = len(self.db[trn_id])-1
            got = False
            while l <= r:
                m = (l+r) // 2
                if int(self.db[trn_id][m]) == cur_node.label:
                    cur_node.support += 1
                    got = True
                    break
                elif int(self.db[trn_id][m]) < cur_node.label:
                    l = m + 1
                else:
                    r = m-1
        if got or (cur_node.label is None):
            for child in cur_node.children:
                self.support_update(cur_node.children[child], trn_id)
    
    def frequent_set_generation(self, cur_node):
        tmp_children = copy.deepcopy(cur_node.children)
        cur_node.children = dict()
        if cur_node.label is not None and cur_node.support < self.threshold:
            cur_node.marker = False
        child_no = 0
        for child in tmp_children:
            ret = self.frequent_set_generation(tmp_children[child])
            if ret > 0:
                child_no += ret
                cur_node.children[child] = tmp_children[child]
        return child_no \
               + cur_node.marker

    def count_freq(self, cur_node, cur_set):
        if cur_node.label is not None:
            cur_set.append(cur_node.label)
            if len(cur_set) == self.cur_level:
                # print(cur_set, " : ", cur_node.support)
                return 1
        cnt = 0
        for child in cur_node.children:
            cnt += self.count_freq(cur_node.children[child], copy.deepcopy(cur_set))
        return cnt
    

    def joining(self, cur_node, cur_set, depth):
        if cur_node.label is not None:
            cur_set.append(cur_node.label)
        if depth == self.cur_level - 1:
            itms = list(cur_node.children.keys())
            # print(itms)
            itms.sort()
            # print(itms)
            for i in range(0, len(itms)):
                for j in range(i+1, len(itms)):
                    self.local_set.append(cur_set+[itms[i], itms[j]])
            return
        for child in cur_node.children:
            tmp_cur_set = copy.deepcopy(cur_set)
            self.joining(cur_node.children[child], tmp_cur_set, depth+1)


class Node():

    def __init__(self):
        self.label = None
        self.support = 0.0
        self.children = dict()
        self.marker = True
        self.depth = None




###################### CALL HERE ###############

dataset_path = '../Files/retail.txt'
dataset_name = 'retail'

th = float(input('Enter minsup in %: '))
MyApriory(dataset_path,th,dataset_name)