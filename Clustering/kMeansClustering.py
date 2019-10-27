import copy

import numpy as np
import csv


class k_means:
    class_label = dict()

    def __init__(self, k, filename, cls_file):
        self.K = k
        self.db = list()
        self.clusters = list()  # or dict()
        self.centers = list()  # or dict()
        self.clusters_dic = dict()
        self.clusterId_tupleId = dict()
        self.read_file(filename)
        cls_file = open(cls_file, 'r')

        id = 0
        for cls in cls_file:
            self.class_label[id] = cls
            id += 1

    def read_file(self, filename):
        file = open(filename, 'r')

        for tuple in file:
            data = tuple.replace('\n', '').replace('\r', '').strip()
            if data == '' or data is None:
                break

            d = data.split(',')
            data = []
            for di in d:
                try:
                    di = float(di)
                    data.append(di)
                except ValueError:
                    # print(di, "Not a float")
                    continue

            self.db.append(data)
        # print(self.db)
        self.npdb = np.array(self.db)
        # print('')
        # print(self.npdb)
        # print(self.npdb[0])
        # print(self.npdb[0][0])
        file.close()

    def k_means_process(self, k):

        # initial centroids

        # centre_ids = np.random.randint(0,len(self.db),k)
        centre_ids = np.random.choice(range(len(self.db)), k, replace=False)
        centroids = list()
        print(centre_ids)
        for ci in centre_ids:
            center = self.db[ci]
            # centroids.append(self.db[ci])
            while center in centroids:
                center = self.db[ci % len(self.db)]
            centroids.append(center)

        print('___')

        pfmt = '{0:5} - {1:5} - '
        # print('Cluster ID', 'Center', 'Cluster Length', '_________________')
        print(pfmt.format('Cluster ID', 'Cluster Length - Centroid'))

        terminate = False
        iteration = 1
        clusters = dict()
        clusters_tupleId = dict()

        while terminate is False:
            print('---', iteration)
            iteration += 1
            clusters = dict()
            clusters_tupleId = dict()
            for ci in range(len(centroids)):
                # print(ci)
                clusters[ci] = []
                clusters_tupleId[ci] = []
            # assigning data-objects
            for tuple_id in range(0, len(self.db)):
                # for di in self.db:
                di = self.db[tuple_id]
                ci_dst = dict()
                for ci in range(len(centroids)):
                    ci_dst[ci] = self.euclid_distance(di, centroids[ci])
                    # print('--',ci,ci_dst[ci])

                distances = list(ci_dst.values())
                centers = list(ci_dst.keys())
                mycluster = centers[distances.index(min(distances))]
                # print(di)
                # print(ci_dst)
                # print('FOUND',mycluster,centroids[mycluster])

                cluster_members = list()
                cluster_memberIds = list()
                if clusters.get(mycluster) is not None:
                    cluster_members = clusters[mycluster]
                    cluster_memberIds = clusters_tupleId[mycluster]
                cluster_members.append(di)
                cluster_memberIds.append(tuple_id)

                clusters[mycluster] = cluster_members
                clusters_tupleId[mycluster] = cluster_memberIds

            # updte cluster centroids
            new_centroids = list()
            for curr_centr in clusters.keys():
                # print('|',curr_centr,'|', centroids[curr_centr]
                #       # , clusters[curr_centr]
                #       , '|',len(clusters[curr_centr]),'|'
                #       )
                print(pfmt.format(str(curr_centr), str(len(clusters[curr_centr]))), end='')
                print(centroids[curr_centr])

                new_centroids.append(np.mean(clusters[curr_centr], axis=0))

            # print(centroids)
            terminate = self.closing_condition(centroids, new_centroids)
            if terminate:
                print('Terminating k-means')
                break
            centroids = new_centroids
            self.clusters_dic = copy.deepcopy(clusters)
        print(self.clusters_dic)

        self.clusterId_tupleId = clusters_tupleId
        print('##########')
        print('cluster id : tuple ids', self.clusterId_tupleId)
        print('...')
        print('id=0', self.clusterId_tupleId[0])

    def euclid_distance(self, data_a, data_b):
        a = np.array(data_a)
        b = np.array(data_b)
        dist = np.linalg.norm(a - b)
        return dist

    def closing_condition(self, prev_centroids, new_centroids):
        terminate = True
        for i in range(len(prev_centroids)):
            dist = self.euclid_distance(prev_centroids[i], new_centroids[i])
            if dist > 0.01:
                terminate = False

        return terminate

    def quality_function(self, purity):
        # for clky in self.cluster_dic:
        #     for ai in self.cluster_dic[clky]:
        #         for
        sil_co = self.silhouette_coefficient()
        sum_sil_co = 0
        count_total = 0
        for idx in sil_co:
            sum_sil_co += sil_co[idx]
            count_total += len(self.clusters_dic[idx])
        dun_co = self.dunn_index()
        sum_dun_co = 0
        count_total_dun = len(dun_co)
        for idx in dun_co:
            sum_dun_co += dun_co[idx]

        # print(sil_co)
        # print(dun_co)
        # print(sum_sil_co, count_total, sum_dun_co, count_total_dun)
        if purity == False:
            return sum_sil_co / count_total, sum_dun_co / count_total_dun
        else:
            return sum_sil_co / count_total, sum_dun_co / count_total_dun, self.determine_purity()

    def silhouette_coefficient(self):
        a_value = dict()
        b_value = dict()
        s_value = dict()
        for clky in self.clusters_dic:
            a_value[clky] = 5050
            b_value[clky] = 5050
            s_value[clky] = 0
            for val_i in self.clusters_dic[clky]:
                # print(val_i, ' At sil ', type(val_i))
                ind_a = 0.0
                for val_j in self.clusters_dic[clky]:
                    ind_a += self.euclid_distance(val_i, val_j)

                ind_a /= (len(self.clusters_dic[clky]) - 1)

                ind_b = float('inf')
                for not_clky in self.clusters_dic:
                    if clky != not_clky:
                        tmp_b = 0
                        for val_k in self.clusters_dic[not_clky]:
                            tmp_b += self.euclid_distance(val_i, val_k)
                        tmp_b /= len(self.clusters_dic[not_clky])
                        ind_b = min(ind_b, tmp_b)

                #     b_value[clky] += ind_b
                #     a_value[clky] += ind_a
                # b_value[clky] /= len(self.clusters[clky])
                # a_value[clky] /= (len(self.clusters[clky])-1)
                #     if (ind_b - ind_a)/(max(ind_b, ind_a)) < 0:
                #         print(ind_a, ind_b)
                s_value[clky] += (ind_b - ind_a) / (max(ind_b, ind_a))
            # s_value[clky] /= (len(self.clusters_dic[clky]))

        # print(b_value, a_value, s_value)
        return s_value

    def dunn_index(self):
        dunn_value = dict()
        for clky in self.clusters_dic:
            diameter = float('-inf')
            separation = float('inf')
            for ai in self.clusters_dic[clky]:
                for bi in self.clusters_dic[clky]:
                    diameter = max(self.euclid_distance(ai, bi), diameter)
                for nonclky in self.clusters_dic:
                    if nonclky != clky:
                        for ci in self.clusters_dic[nonclky]:
                            separation = min(self.euclid_distance(ai, ci), separation)
            dunn_value[clky] = separation / diameter
        return dunn_value

    def determine_purity(self):
        purity_val = 0

        total_instance = 0

        for clky in self.clusters_dic:
            tmp_dic = dict()
            total_instance += len(self.clusters_dic[clky])
            for val_lst in self.clusters_dic[clky]:
                for val in val_lst:
                    if self.class_label[val] not in tmp_dic:
                        tmp_dic[self.class_label[val]] = 0
                    tmp_dic[self.class_label[val]] += 1
            mx_val = 0
            for cls in tmp_dic:
                mx_val = max(mx_val, tmp_dic[cls])

            purity_val += mx_val
        return purity_val / total_instance


#
#
# kk = k_means(3, 'dataset/Iris/iris.txt', '')
# # kk = k_means(5,'../k_mean/WholeSale/Wholesale.csv')
# # kk = k_means(3,'../DecisionTree/Dataset/wine/wine.data')
#
# kk.k_means_process(kk.K)
# sil_val , dun_val = kk.quality_function()
# print(sil_val, dun_val, ' Quality..')
# kk = k_means(3, '../Clustering/dataset/WholeSale/Wholesale.csv')
# kk.k_means_process(kk.K)
