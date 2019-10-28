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
        [True, 'dataset/Iris/iris.attr', '../Clustering/dataset/Iris/iris.data',
         '../Clustering/dataset/Iris/iris.class', 'Iris'],
        # [True, '../Clustering/dataset/glass/glass.attr', '../Clustering/dataset/glass/glass.data',
        #  '../Clustering/dataset/glass/glass.class', 'Glass'],
        # [True, '../Clustering/dataset/diabetes/diabetes.attr', '../Clustering/dataset/diabetes/diabetes.data',
        #  '../Clustering/dataset/diabetes/diabetes.class', 'Diabetes'],
        # [True, '../Clustering/dataset/banknote/banknote.attr', '../Clustering/dataset/banknote/banknote.data',
        #  '../Clustering/dataset/banknote/banknote.class', 'Banknote'],
        # [True, '../Clustering/dataset/aggregation/Aggregation.attr','../Clustering/dataset/aggregation/Aggregation.data', '../Clustering/dataset/aggregation/Aggregation.class','Aggregation']
        # [False, '../Clustering/dataset/WholeSale/wholesale.attr', '../Clustering/dataset/WholeSale/Wholesale.csv',
        #  '../Clustering/dataset/WholeSale/wholesale.class', 'Wholesale']
        # [False, '../Clustering/dataset/breast/breast.attr', '../Clustering/dataset/breast/breast.data',
        #  '../Clustering/dataset/breast/breast.class', 'Breast Cancer']

    ]

    resultFile = 'result_iris_x.csv'
    result = open(resultFile, 'a')
    result.close()

    buff = 'dataset, k, kmd_sil_co, kmd_purity, kmd_dun_co, kmd_time, kmn_sil_co, kmn_purity, kmn_dun_co, kmn_time'
    # result.write(buff+'\n')

    for tup in file:
        # print(tup[2])
        for k in [20,50,100,150]:
            # k = 3
            data = [tup[4], str(k)]
            print( 'Dataset', tup[4], 'k', k)
            kmd = Medoid(k, tup[1], tup[2], tup[3])
            start_time = time.time()
            if tup[0] == True:
                kmd_sil_co, kmd_dun_co, kmd_purity = kmd.run_algorithm(tup[0])
            else:
                kmd_sil_co, kmd_dun_co = kmd.run_algorithm(tup[0])
                kmd_purity = 0
            end_time = time.time()
            kmd_time = end_time - start_time

            print('KMD: ', kmd_sil_co, kmd_purity, kmd_dun_co, kmd_time)
            data.append(kmd_sil_co)
            data.append(kmd_purity)
            data.append(kmd_dun_co)
            data.append(kmd_time)

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
