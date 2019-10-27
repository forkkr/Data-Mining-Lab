import time

from Clustering.kMeansClustering import k_means
from Clustering.k_medoid import Medoid


if __name__ == '__main__':

    # attr_file = 'dataset/Iris/iris.attr'
    # obj_file = 'dataset/Iris/iris.txt'
    # attr_file = 'dataset/banknote/banknote.attr'
    # obj_file = 'dataset/banknote/banknote.csv'
    # attr_file = 'dataset/breast/breast.attr'
    # obj_file = 'dataset/breast/breast.data'

    # attr_file = '../Clustering/dataset/diabetes/diabetes.attr'
    # obj_file = '../Clustering/dataset/diabetes/diabetes.csv'
    # cls_file = ''
    # kmd = Medoid(2, attr_file, obj_file, cls_file)
    # start_time = time.time()
    # sil_co, dun_co = kmd.run_algorithm(True)
    # print(sil_co, dun_co)
    # end_time = time.time()
    # print('Total time: ', end_time-start_time)

    file = [
        [True, 'dataset/Iris/iris.attr', '../Clustering/dataset/Iris/iris.data', '../Clustering/dataset/Iris/iris.class'],
            [ True, '../Clustering/dataset/glass/glass.attr', '../Clustering/dataset/glass/glass.data', '../Clustering/dataset/glass/glass.class'],
            [True, '../Clustering/dataset/diabetes/diabetes.attr', '../Clustering/dataset/diabetes/diabetes.data', '../Clustering/dataset/diabetes/diabetes.class'],
            [True, '../Clustering/dataset/banknote/banknote.attr', '../Clustering/dataset/banknote/banknote.data', '../Clustering/dataset/banknote/banknote.class'],
            [True, '../Clustering/dataset/aggregation/Aggregation.attr', '../Clustering/dataset/aggregation/Aggregation.data', '../Clustering/dataset/aggregation/Aggregation.class'],
            [False, '../Clustering/dataset/WholeSale/wholesale.attr', '../Clustering/dataset/WholeSale/Wholesale.csv', '../Clustering/dataset/WholeSale/wholesale.class']
    ]

    for tup in file:
        # print(tup[2])
        for k in range(2, 3):
            kmd = Medoid(k, tup[1], tup[2], tup[3])
            start_time = time.time()
            if tup[0] == True:
                kmd_sil_co, kmd_dun_co, kmd_purity = kmd.run_algorithm(tup[0])
            else:
                kmd_sil_co, kmd_dun_co = kmd.run_algorithm(tup[0])
                kmd_purity = 0
            end_time = time.time()
            kmd_time = end_time-start_time

            print('KMD: ', kmd_sil_co, kmd_purity, kmd_dun_co, kmd_time)

            kk = k_means(k, tup[2], tup[3])
            start_time = time.time()
            kk.k_means_process(kk.K)
            if tup[0] == True:
                kmn_sil_co, kmn_dun_co, kmn_purity = kk.quality_function(tup[0])
            else:
                kmn_sil_co, kmn_dun_co = kk.quality_function(tup[0])
                kmn_purity = 0
            end_time = time.time()
            kmn_time = end_time - start_time

            print('KMN :', kmn_sil_co, kmn_purity, kmn_dun_co, kmn_time)

            print('\n ------------------------------ \n')



