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

    # dataset_file = '../BayesianClassification/Dataset/Iris/iris.data'
    # attr_file = '../BayesianClassification/Dataset/Iris/iris_attr.txt'
    # tst_file = '../BayesianClassification/Dataset/Iris/iris_tst.data'

    dataset_file = 'Dataset/Car/car.data'
    attr_file = 'Dataset/Car/car_attr.txt'
    tst_file = 'Dataset/Car/car_tst.data'

    # dataset_file = 'Dataset/Iris/iris.data'
    # attr_file = 'Dataset/Iris/iris_attr.txt'
    # tst_file = 'Dataset/Iris/iris_tst.data'

    # totalsize = shuffle(dataset_file)

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

    random.shuffle(ids)
    # print(ids)

    with open(outputFile, 'w') as outFile:
        for i in ids:
            outFile.write(temp[i])
            outFile.write('\n')

    totalsize = len(ids)
    dataset_file = outputFile

    k = 10
    partition_size = totalsize // k
    start = 0
    for i in range(0, k):
        test_tuples = ids[start:start+partition_size]
        print(test_tuples, len(test_tuples))
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
        bayes = BayesianClassifier(trainFile, attr_file, 'unacc')
        # bayes = BayesianClassifier(trainFile, attr_file, 'Iris-setosa')
        bayes.test_run(testFile)
        print('')

        start += partition_size
        if start >= totalsize:
            start = totalsize - 1
            partition_size = 0

    # bayes = BayesianClassifier(trainFile, attr_file, 'unacc')
    # bayes.test_run(testFile)
