import time

from Clustering.kMeansClustering import k_means
from Clustering.k_medoid import Medoid
from Clustering.kmeans_improved import kmeans_improved

if __name__ == '__main__':

    file = [
        [True, 'dataset/Iris/iris.attr', '../Clustering/dataset/Iris/iris.data',
         '../Clustering/dataset/Iris/iris.class', 'Iris'],
        [True, '../Clustering/dataset/glass/glass.attr', '../Clustering/dataset/glass/glass.data',
         '../Clustering/dataset/glass/glass.class', 'Glass'],
        [True, '../Clustering/dataset/diabetes/diabetes.attr', '../Clustering/dataset/diabetes/diabetes.data',
         '../Clustering/dataset/diabetes/diabetes.class', 'Diabetes'],
        [True, '../Clustering/dataset/banknote/banknote.attr', '../Clustering/dataset/banknote/banknote.data',
         '../Clustering/dataset/banknote/banknote.class', 'Banknote'],
        [True, '../Clustering/dataset/aggregation/Aggregation.attr',
         '../Clustering/dataset/aggregation/Aggregation.data', '../Clustering/dataset/aggregation/Aggregation.class',
         'Aggregation'],
        [False, '../Clustering/dataset/WholeSale/wholesale.attr', '../Clustering/dataset/WholeSale/Wholesale.csv',
         '../Clustering/dataset/WholeSale/wholesale.class', 'Wholesale'],
        [False, '../Clustering/dataset/breast/breast.attr', '../Clustering/dataset/breast/breast.data',
         '../Clustering/dataset/breast/breast.class', 'Breast Cancer']

    ]

    resultFile = 'k_means_comp.csv'
    result = open(resultFile, 'a')
    result.close()

    buff = 'dataset, k, old_sil_co, old_purity, old_dun_co, old_time, imp_sil_co, imp_purity, imp_dun_co, imp_time'
    # result.write(buff+'\n')

    for tup in file:
        # print(tup[2])
        for k in [3, 5, 10, 20]:
            # k = 3
            data = [tup[4], str(k)]
            print('Dataset', tup[4], 'k', k)

            # kmd = Medoid(k, tup[1], tup[2], tup[3])
            # start_time = time.time()
            # if tup[0] == True:
            #     kmd_sil_co, kmd_dun_co, kmd_purity = kmd.run_algorithm(tup[0])
            # else:
            #     kmd_sil_co, kmd_dun_co = kmd.run_algorithm(tup[0])
            #     kmd_purity = 0
            # end_time = time.time()
            # kmd_time = end_time - start_time
            #
            # print('KMD: ', kmd_sil_co, kmd_purity, kmd_dun_co, kmd_time)
            # data.append(kmd_sil_co)
            # data.append(kmd_purity)
            # data.append(kmd_dun_co)
            # data.append(kmd_time)

            kk = k_means(k, tup[2], tup[3])
            start_time = time.time()
            kk.k_means_process(kk.K)
            if tup[0]:
                kmn_sil_co, kmn_dun_co, kmn_purity = kk.quality_function(tup[0])
            else:
                kmn_sil_co, kmn_dun_co = kk.quality_function(tup[0])
                kmn_purity = 0
            end_time = time.time()
            kmn_time = end_time - start_time

            print('KMN version 1.0:', 'Sil', round(kmn_sil_co, 4), 'Purity', round(kmn_purity, 4), 'Dunn',
                  round(kmn_dun_co, 4), 'Time', round(kmn_time, 4))
            data.append(kmn_sil_co)
            data.append(kmn_purity)
            data.append(kmn_dun_co)
            data.append(kmn_time)

            kk = kmeans_improved(k, tup[2], tup[3])
            start_time = time.time()
            kk.k_means_process(kk.K)
            if tup[0]:
                kmn_sil_co, kmn_dun_co, kmn_purity = kk.quality_function(tup[0])
            else:
                kmn_sil_co, kmn_dun_co = kk.quality_function(tup[0])
                kmn_purity = 0
            end_time = time.time()
            kmn_time = end_time - start_time

            print('KMN improved :', 'Sil', round(kmn_sil_co, 4), 'Purity', round(kmn_purity, 4), 'Dunn',
                  round(kmn_dun_co, 4), 'Time', round(kmn_time, 4))
            data.append(kmn_sil_co)
            data.append(kmn_purity)
            data.append(kmn_dun_co)
            data.append(kmn_time)

            result = open(resultFile, 'a')
            for d in data:
                result.write(str(d) + ', ')
            result.write('\n')
            result.close()
            print('\n ------------------------------ \n')
