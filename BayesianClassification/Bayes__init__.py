from BayesianClassification.Bayesian import BayesianClassifier

if __name__=='__main__':

    dataset_file = 'Dataset/BuysComputer/buysComp.data'
    attr_file = 'Dataset/BuysComputer/buysComp_attr.txt'
    tst_file = 'Dataset/Car/car_tst.data'

    # dataset_file = 'Dataset/Car/car.data'
    # attr_file = 'Dataset/Car/car_attr.txt'
    # tst_file = 'Dataset/Car/car_tst.data'

    # dataset_file = 'Dataset/Iris/iris.data'
    # attr_file = 'Dataset/Iris/iris_attr.txt'
    # tst_file = 'Dataset/Iris/iris_tst.data'

    bayes = BayesianClassifier(dataset_file, attr_file)
    bayes.test_run(dataset_file)