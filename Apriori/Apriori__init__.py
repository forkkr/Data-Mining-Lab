import time

from Apriori.DataSet import DatasetProcessing as dsp
from Apriori.AprioriAlgorithm import AprioriAlgorithm

if __name__ == '__main__':
    dsp('../Files/mushroom.txt').preprocess()
    start_time = time.time()
    AprioriAlgorithm(2000).apriori_algorithm()
    end_time = time.time()
    print('Total Time: ',end_time-start_time)

