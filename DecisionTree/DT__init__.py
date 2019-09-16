from DecisionTree.DT_Classifier import DecisionTreeClassifier

if __name__=='__main__':
    # dataset_file = 'tennis.csv'
    # attr_file = 'tennis_attr.txt'
    # dataset_file = 'buys_comp.csv'
    # attr_file = 'buys_comp_attr.txt'
    # tst_file = 'buys_comp_tst.txt'

    # dataset_file = 'Dataset/Car/car.data'
    # attr_file = 'Dataset/Car/car_attr.txt'
    # tst_file = 'Dataset/Car/car_tst.data'

    dataset_file = 'Dataset/Iris/iris.data'
    attr_file = 'Dataset/Iris/iris_attr.txt'
    tst_file = 'Dataset/Iris/iris_tst.data'

    DTc = DecisionTreeClassifier(dataset_file, attr_file)
    DTc.induction()
    DTc.classifier(tst_file)


