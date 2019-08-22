import time

from Apriori.DataSet import DatasetProcessing as dsp
from Apriori.AprioriAlgorithm import AprioriAlgorithm

if __name__ == '__main__':
    dsp('../Files/mushroom.txt').preprocess()
    start_time = time.time()
    tot_pattern = AprioriAlgorithm(.7).apriori_algorithm()
    end_time = time.time()
    print('total pattern: ', tot_pattern)
    print('Total Time: ',end_time-start_time)

