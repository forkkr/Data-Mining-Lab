import copy
import numpy as np


class kmeans_improved:
    class_label = dict()

    def __init__(self, k, filename, cls_file):
        self.K = k
        self.db = list()
        # self.clusters = list()  # or dict()
        self.centers = list()  # or dict()
        self.clusters_dic = dict()
        self.clusterId_tupleId = dict()
        self.tupleId_clusterId = dict()

        self.read_file(filename)
        cls_file = open(cls_file, 'r')

        id = 0
        for cls in cls_file:
            self.class_label[id] = cls
            id += 1

        for id in range(0, len(self.db)):
            self.tupleId_clusterId[id] = None

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
        file.close()

    def k_means_process(self, k):

        # initial centroids

        # centre_ids = np.random.randint(0,len(self.db),k)
        centre_ids = np.random.choice(range(len(self.db)), k, replace=False)
        centroids = list()
        # print(centre_ids)
        for ci in centre_ids:
            center = self.db[ci]
            ccc = ci
            while center in centroids:
                center = self.db[ccc % len(self.db)]
                ccc += 1
            centroids.append(center)
        print('___')
        print('initial centroids', centroids)

        # clusters = dict()
        for cid in range(len(centroids)):
            self.clusters_dic[cid] = []

        # initial assigning:
        for tid in range(0, len(self.db)):
            di = self.db[tid]
            ci_dst = dict()
            for ci in range(len(centroids)):
                ci_dst[ci] = self.euclid_distance(di, centroids[ci])
            distances = list(ci_dst.values())
            centers = list(ci_dst.keys())
            mycluster = centers[distances.index(min(distances))]

            self.tupleId_clusterId[tid] = mycluster
            existing_members = self.clusters_dic[mycluster]
            if existing_members is None:
                existing_members = [self.db[tid]]
            else:
                existing_members.append(self.db[tid])
            self.clusters_dic[mycluster] = existing_members

        print('initial clusters',
              len(self.clusters_dic[0]), len(self.clusters_dic[1]), len(self.clusters_dic[2]))

        new_centroids = list()
        for curr_centr in self.clusters_dic.keys():
            new_centroids.append(np.mean(self.clusters_dic[curr_centr], axis=0))
        centroids = new_centroids

        pfmt = '{0:5} - {1:5} - '
        # print('Cluster ID', 'Center', 'Cluster Length', '_________________')
        print(pfmt.format('Cluster ID', 'Cluster Length - Centroid'))

        terminate = False
        iteration = 1

        clusters_tupleId = dict()
        clusters = copy.deepcopy(self.clusters_dic)

        while terminate is False:
            # print('---', iteration)
            iteration += 1

            # clusters = copy.deepcopy(self.clusters_dic)
            old_centroids = copy.deepcopy(centroids)

            clusters_tupleId = dict()
            for ci in range(len(centroids)):
                clusters_tupleId[ci] = []

            # assigning data-objects
            for tuple_id in range(0, len(self.db)):
                # for di in self.db:
                di = self.db[tuple_id]
                old_clstr_id = self.tupleId_clusterId[tuple_id]

                ci_dst = dict()
                for cid in range(len(centroids)):
                    ci_dst[cid] = self.euclid_distance(di, centroids[cid])
                    # print('--',ci,ci_dst[ci])

                distances = list(ci_dst.values())
                centers = list(ci_dst.keys())
                new_cluser_id = centers[distances.index(min(distances))]
                self.tupleId_clusterId[tuple_id] = new_cluser_id
                # print(di, 'new clstr id---', new_cluser_id)

                if old_clstr_id != new_cluser_id:
                    # update_centroids(old_cluster, new_cluser_id)
                    # print('changed', di, old_clstr_id, new_cluser_id,
                    #       # centroids, old_centroids
                    #       )
                    old_clstr_members = clusters[old_clstr_id]
                    old_clstr_members.remove(self.db[tuple_id])
                    clusters[old_clstr_id] = old_clstr_members

                    new_clstr_members = clusters[new_cluser_id]
                    new_clstr_members.append(self.db[tuple_id])
                    clusters[new_cluser_id] = new_clstr_members

                    centroids[old_clstr_id] = np.mean(old_clstr_members, axis=0)
                    centroids[new_cluser_id] = np.mean(new_clstr_members, axis=0)

                cluster_members = list()
                cluster_memberIds = list()
                if clusters.get(new_cluser_id) is not None:
                    cluster_members = clusters[new_cluser_id]
                    cluster_memberIds = clusters_tupleId[new_cluser_id]
                cluster_members.append(di)
                cluster_memberIds.append(tuple_id)

                clusters[new_cluser_id] = cluster_members
                clusters_tupleId[new_cluser_id] = cluster_memberIds

            # updte cluster centroids
            new_centroids = list()
            for curr_centr in clusters.keys():
                new_centroids.append(np.mean(clusters[curr_centr], axis=0))

            # print(centroids)
            terminate = self.closing_condition(centroids, old_centroids)
            if terminate:
                print('Terminating k-means at iteration: ', iteration)
                break

            self.clusters_dic = copy.deepcopy(clusters)
            clusters = dict()

        # for cid in range(len(centroids)):

        self.clusterId_tupleId = clusters_tupleId
        # print('___')
        # print('Final centroids', centroids)
        print('Final clusters',
              len(self.clusters_dic[0]), len(self.clusters_dic[1]), len(self.clusters_dic[2]))

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

        for clky in self.clusterId_tupleId:
            tmp_dic = dict()
            total_instance += len(self.clusterId_tupleId[clky])
            for val in self.clusterId_tupleId[clky]:
                # for val in val_lst:
                if self.class_label[val] not in tmp_dic:
                    tmp_dic[self.class_label[val]] = 0
                tmp_dic[self.class_label[val]] += 1
            mx_val = 0
            for cls in tmp_dic:
                mx_val = max(mx_val, tmp_dic[cls])

            purity_val += mx_val

        print('total instances: ', total_instance)
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
# kk = kmeans_improved(3, '../Clustering/dataset/breast/breast.data',
#                      '../Clustering/dataset/breast/breast.class')
# kk.k_means_process(kk.K)
