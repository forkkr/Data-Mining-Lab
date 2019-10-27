import copy

import numpy as np
import csv

class k_means:

    def __init__(self,k,filename):
        self.K = k
        self.db = list()
        self.clusters = list()  # or dict()
        self.centers = list()     # or dict()
        self.cluster_dic = dict()
        self.read_file(filename)


    def read_file(self, filename):
        file  = open(filename,'r')

        for tuple in file:
            data = tuple.replace('\n','').replace('\r','').strip()
            if data=='' or data is None:
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

    def k_means_process(self,k):

        # initial centroids

        # centre_ids = np.random.randint(0,len(self.db),k)
        centre_ids = np.random.choice(range(len(self.db)), k, replace=False)
        centroids = list()
        print(centre_ids)
        for ci in centre_ids:
            center = self.db[ci]
            # centroids.append(self.db[ci])
            while center in centroids:
                center = self.db[ci%len(self.db)]
            centroids.append(center)

        print('___')


        pfmt = '{0:5} - {1:5} - '
        # print('Cluster ID', 'Center', 'Cluster Length', '_________________')
        print(pfmt.format('Cluster ID','Cluster Length - Centroid'))

        terminate = False
        iteration = 1
        while terminate is False:
            print('---',iteration)
            iteration+=1
            clusters = dict()
            for ci in range(len(centroids)):
                # print(ci)
                clusters[ci] = []
            # assigning data-objects
            for di in self.db:
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
                if clusters.get(mycluster) is not None:
                    cluster_members = clusters[mycluster]
                cluster_members.append(di)
                clusters[mycluster] = cluster_members

            # updte cluster centroids
            new_centroids = list()
            for curr_centr in clusters.keys():
                # print('|',curr_centr,'|', centroids[curr_centr]
                #       # , clusters[curr_centr]
                #       , '|',len(clusters[curr_centr]),'|'
                #       )
                print(pfmt.format(str(curr_centr), str(len(clusters[curr_centr]))),end='')
                print(centroids[curr_centr])

                new_centroids.append(np.mean(clusters[curr_centr], axis=0))


            # print(centroids)
            terminate = self.closing_condition(centroids, new_centroids)
            if terminate:
                print('Terminating k-means')
                break
            centroids = new_centroids
            self.cluster_dic = copy.deepcopy(clusters)
        print(self.cluster_dic)

    def euclid_distance(self, data_a,data_b):
        a = np.array(data_a)
        b = np.array(data_b)
        dist = np.linalg.norm(a-b)
        return dist

    def closing_condition(self,prev_centroids,new_centroids):
        terminate = True
        for i in range(len(prev_centroids)):
            dist = self.euclid_distance(prev_centroids[i],new_centroids[i])
            if dist>0.01:
                terminate = False

        return terminate



    def quality_function(self):
        pass

kk = k_means(3, 'dataset/Iris/iris.data')
# kk = k_means(5,'../k_mean/WholeSale/Wholesale customers data.csv')
# kk = k_means(3,'../DecisionTree/Dataset/wine/wine.data')

kk.k_means_process(kk.K)