import time

from Clustering.k_medoid import Medoid


if __name__ == '__main__':

    # attr_file = 'dataset/Iris/iris_attr.txt'
    # obj_file = 'dataset/Iris/iris.data'
    attr_file = 'dataset/breast/breast.attr'
    obj_file = 'dataset/breast/breast.data'
    kmd = Medoid(2, attr_file, obj_file)
    start_time = time.time()
    kmd.run_algorithm()
    end_time = time.time()
    print('Total time: ', end_time-start_time)
