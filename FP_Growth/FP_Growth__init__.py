import time,os,errno

from FP_Growth.FPGrowthAlgorithm import FPGrowth
from FP_Growth.DataSet import DatasetProcessing


def ffopen(fileLocation, mode, title=None):
    # if not os.path.exists(os.path.dirname(fileLocation)):
    if not os.path.exists(fileLocation):
        try:
            os.makedirs(os.path.dirname(fileLocation))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
        f = open(fileLocation, mode)
        if title is None:
            title = input('Creating New File, Enter Title: ')
        f.write(title)
        f.close()

    f = open(fileLocation, mode)
    return f

if __name__ == '__main__':

    datasets = ['mushroom.txt',
                'chess.txt',
                'retail.txt',
                'kosarak.txt']

    for d in datasets:
        d = d.replace('.txt', '')
        print('Dataset', d)
        minsup = 100.0
        while minsup > 0:
            minsup = float(input('Enter min_sup in %: '))
            if minsup<=0.0:
                break
            threshold = minsup / 100.0
            filename = '../Files/' + d + '.txt'
            DatasetProcessing(filename).preprocess()

            output_file = '../Files/result_fp.csv'
            title = 'dataset,min_sup %,No. of Conditional Trees, Total Patterns,FP_Growth time (s)\n'
            outf = ffopen(output_file, 'a', title)
            result = FPGrowth(threshold).fp_growth()
            print(result)
            result_s = list()
            for i in range(0, len(result)):
                result_s.append(str(result[i]))

            buffer = ','.join(result_s)
            buffer_s = d + ',' + str(minsup) + ',' + buffer + '\n'
            print('writing into file...')
            outf.write(buffer_s)
            outf.close()

    threshold = float(input('Enter min_sup in %: '))/100.0
    filename = '../Files/sign.txt'
    # filename = '../Files/sample.txt'
    # filename = '../Files/chess.txt'

    start_time = time.time()
    DatasetProcessing(filename).preprocess()
    FPGrowth(threshold).fp_growth()
    end_time = time.time()
    print('Total Time: ', end_time - start_time)
