import time

from FP_Growth.FPGrowthAlgorithm import FPGrowth
from FP_Growth.DataSet import DatasetProcessing

if __name__ == '__main__':
    threshold = 0.2
    filename = '../Files/mushroom.txt'
    start_time = time.time()
    DatasetProcessing(filename).preprocess()
    FPGrowth(threshold).fp_growth()
    end_time = time.time()
    print('Total Time: ', end_time - start_time)
