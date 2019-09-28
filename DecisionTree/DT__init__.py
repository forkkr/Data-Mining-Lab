import time

from DecisionTree.DT_Classifier import DecisionTreeClassifier

class DT_INIT():

    def run_DT_model(self, dataset_file, tst_file, attr_file, reverse_order, true_class,threshold):
        start_time = time.time()
        DTc = DecisionTreeClassifier(dataset_file, attr_file, reverse_order, true_class, threshold)
        DTc.induction()
        mid_time = time.time()
        # print("Time at build phase: ", mid_time - start_time)
        tot, accurate, P, TP, FP = DTc.classifier(tst_file)
        end_time = time.time()
        # print('Time at classify phase: ', end_time - mid_time)
        # print('Total time: ', end_time - start_time)
        return tot, accurate, P, TP, FP, end_time-start_time




# if __name__=='__main__':
#     # dataset_file = 'tennis.csv'
#     # attr_file = 'tennis_attr.txt'
#     # dataset_file = 'buys_comp.csv'
#     # attr_file = 'buys_comp_attr.txt'
#     # tst_file = 'buys_comp_tst.txt'
#
#     # dataset_file = 'Dataset/Car/car.data'
#     # attr_file = 'Dataset/Car/car_attr.txt'
#     # tst_file = 'Dataset/Car/car_tst.data'
#
#     # dataset_file = 'Dataset/Iris/iris.data'
#     # attr_file = 'Dataset/Iris/iris_attr.txt'
#     # tst_file = 'Dataset/Iris/iris_tst.data'
#
#     # dataset_file = 'Dataset/Abalone/abalone.data'
#     # attr_file = 'Dataset/Abalone/abalone_attr.txt'
#     # tst_file = 'Dataset/Abalone/abalone_tst.data'
#
#     # dataset_file = 'Dataset/BreastCancer/breast-cancer.data'
#     # attr_file = 'Dataset/BreastCancer/breast-cancer-attr.txt'
#     # tst_file = 'Dataset/BreastCancer/breast-cancer-tst.data'
#
#     dataset_file = 'Dataset/Adult/adult.data'
#     attr_file = 'Dataset/Adult/adult-attr.txt'
#     tst_file = 'Dataset/Adult/adult.test'
#
#     start_time = time.time()
#     DTc = DecisionTreeClassifier(dataset_file, attr_file)
#     DTc.induction()
#     mid_time = time.time()
#     print("Time at build phase: ", mid_time - start_time)
#     DTc.classifier(tst_file)
#     end_time = time.time()
#     print('Time at classify phase: ', end_time - mid_time)
#     print('Total time: ', end_time - start_time)


