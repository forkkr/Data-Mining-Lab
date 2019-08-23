import copy,math,time,os,errno

from Apriori.DataSet import DatasetProcessing as dsp
from Apriori.AprioriAlgorithm import AprioriAlgorithm
from FP_Growth.DataSet import DatasetProcessing as dspf
from FP_Growth.FPGrowthAlgorithm import FPGrowth

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

    datasets = [
                'mushroom.txt',
                'chess.txt',
                'retail.txt',
                'kosarak.txt']

    for d in datasets:
        d = d.replace('.txt','')
        print('Dataset',d)

        filename = '../Files/' + d + '.txt'
        dsp(filename).preprocess()
        dspf(filename).preprocess()

        # output_file = '../Files/' + d + '_apriori.csv'
        output_file = '../Files/result_.csv'
        title = 'dataset,min_sup %,Total Candidates,Total Patterns,Apriori time (s),' \
                'No. of Conditional Trees, Total Patterns,FP_Growth time (s)\n'
        outf = ffopen(output_file, 'a', title)

        for i in range(0,6):
            minsup = float(input('Enter min_sup in %: '))

            if minsup<=0.0:
                break
            threshold = minsup / 100.0

            result = AprioriAlgorithm(threshold).apriori_algorithm()
            print('Apriori:',result)
            result_s = list()
            for i in range(0, len(result)):
                result_s.append(str(result[i]))

            result = FPGrowth(threshold).fp_growth()
            print('FP:',result)
            for i in range(0, len(result)):
                result_s.append(str(result[i]))

            buffer = ','.join(result_s)
            buffer_s = d + ',' + str(minsup) + ',' + buffer + '\n'
            print('writing into file...')
            outf.write(buffer_s)

        outf.close()



    # threshold = float(input('Enter min_sup in %: '))/100.0
    # filename = '../Files/retail.txt'
    # # filename = '../Files/sample.txt'
    # # filename = '../Files/chess.txt'
    #
    # dsp(filename).preprocess()
    # start_time = time.time()
    # tot_pattern = AprioriAlgorithm(threshold).apriori_algorithm()
    # end_time = time.time()
    # # print('total pattern: ', tot_pattern)
    # # print('Total Time: ',end_time-start_time)

