import time

from Apriori.DataSet import DatasetProcessing as dsp
from Apriori.AprioriAlgorithm import AprioriAlgorithm

if __name__ == '__main__':
    threshold = float(input('Enter min_sup in %: '))/100.0
    filename = '../Files/retail_item.txt'
    # filename = '../Files/sample.txt'
    # filename = '../Files/chess.txt'

    dsp(filename).preprocess()
    start_time = time.time()
    tot_pattern = AprioriAlgorithm(threshold).apriori_algorithm()
    end_time = time.time()
    print('total pattern: ', tot_pattern)
    print('Total Time: ',end_time-start_time)

