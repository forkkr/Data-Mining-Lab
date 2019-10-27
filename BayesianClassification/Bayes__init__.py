from BayesianClassification.Bayesian import BayesianClassifier
import random


def shuffle(fileName):
    outputFile = fileName.replace('.data', '_shf.data')
    temp = []
    ids = []
    with open(fileName, 'r') as inFile:
        tid = 0
        for entry in inFile:

            entry = entry.strip().replace('\n', '').replace('\r', '')
            if entry == '' or entry is None:
                break
            ids.append(tid)
            temp.append(entry)
            tid += 1

    random.shuffle(ids)
    print(ids)

    with open(outputFile, 'w') as outFile:
        for i in ids:
            outFile.write(temp[i])
            outFile.write('\n')

    return len(ids)


if __name__ == '__main__':

    dataset_file = '../BayesianClassification/Dataset/BuysComputer/buysComp.data'
    attr_file = '../BayesianClassification/Dataset/BuysComputer/buysComp_attr.txt'

    dataset_file = '../BayesianClassification/Dataset/PlayTennis/tennis.data'
    attr_file = '../BayesianClassification/Dataset/PlayTennis/tennis_attr.txt'

    dataset_file = 'Dataset/Car/car.data'
    attr_file = 'Dataset/Car/car_attr.txt'

    #
    # dataset_file = 'Dataset/Iris/iris.txt'
    # attr_file = 'Dataset/Iris/iris.attr'

    #
    # dataset_file = '../BayesianClassification/Dataset/Mushroom/mushroom.csv'
    # attr_file = '../BayesianClassification/Dataset/Mushroom/mushroom_attrs.txt'

    # TRUE_CLASS = 'Iris-setosa' #Iris
    TRUE_CLASS = 'unacc' #car
    # TRUE_CLASS = 'e' #mushroom

    outputFile = dataset_file.replace('.data', '_shf.data')
    temp = []
    ids = []
    with open(dataset_file, 'r') as inFile:
        tid = 0
        for entry in inFile:

            entry = entry.strip().replace('\n', '').replace('\r', '')
            if entry == '' or entry is None:
                break
            ids.append(tid)
            temp.append(entry)
            tid += 1

    for i in range(0,2):
        # print('Before', ids)
        random.shuffle(ids)
        print('After', ids)


    with open(outputFile, 'w') as outFile:
        for i in ids:
            outFile.write(temp[i])
            outFile.write('\n')

    totalsize = len(ids)
    dataset_file = outputFile



    k = 10
    partition_size = totalsize // k
    start = 0

    Totals = []
    Corrects = []
    Ps = []
    TPs = []
    FPs = []

    for i in range(0, k):
        test_tuples = ids[start:start + partition_size]
        # print(test_tuples, len(test_tuples))
        print(len(test_tuples))
        if len(test_tuples) <= 0:
            break

        testFile = '../BayesianClassification/Dataset/test.txt'
        trainFile = '../BayesianClassification/Dataset/train.txt'

        with open(testFile, 'w') as testf, open(trainFile, 'w') as trainf:
            for i in ids:
                if i in test_tuples:
                    testf.write(temp[i])
                    testf.write('\n')
                else:
                    trainf.write(temp[i])
                    trainf.write('\n')
        bayes = BayesianClassifier(trainFile, attr_file, TRUE_CLASS)
        # bayes = BayesianClassifier(trainFile, attr_file, 'Iris-setosa')
        total, correct, P, TP, FP, accuracy, precision, recall, fscore = bayes.test_run(testFile)
        Ps.append(P)
        Totals.append(total)
        Corrects.append(correct)
        TPs.append(TP)
        FPs.append(FP)
        print('')

        start += partition_size
        if start >= totalsize:
            start = totalsize - 1
            partition_size = 0

    # bayes = BayesianClassifier(trainFile, attr_file, 'unacc')
    # bayes.test_run(testFile)
    print(sum(Totals), sum(Corrects))
    print(sum(Ps), sum(TPs), sum(FPs))
    print('Accuracy: ', round(sum(Corrects) * 1.0 / sum(Totals), 4))
    prec = sum(TPs) * 1.0 / (sum(TPs) + sum(FPs))
    print('Precision: ', round(prec, 4))
    rec = sum(TPs) * 1.0 / sum(Ps)
    print('Recall: ', round(rec, 4))
    print('F-score: ', round((2*prec*rec/(prec+rec)), 4))
