from DecisionTree.K_Folds import CV


if __name__ == '__main__':
    dataset = [
        ['Car', 1728, 'Dataset/Car/car.data', 'Dataset/Car/car_attr.txt', 0, 'unacc'],
        ['Iris', 150, 'Dataset/Iris/iris.data','Dataset/Iris/iris_attr.txt', 0, 'Iris-versicolor'],
        ['Mushroom', 8124, 'Dataset/Mushroom/agaricus-lepiota.data', 'Dataset/Mushroom/agaricus-lepiota-attr.txt', 1, 'p'],
        # ['Anneal', 798, 'Dataset/Anneal/anneal.data', 'Dataset/Anneal/anneal.attr', 0]
        ['Abalone', 4177, 'Dataset/Abalone/abalone.data', 'Dataset/Abalone/abalone_attr.txt', 0, '9'],
        ['Breast Cancer', 286, 'Dataset/BreastCancer/breast-cancer.data', 'Dataset/BreastCancer/breast-cancer-attr.txt', 1, 'recurrence-events'],
        ['Heart Disease', 303, 'Dataset/HeartDisease/processed.cleveland.data', 'Dataset/HeartDisease/heart-disease.attr', 0, '0'],
        ['Credit Approval', 690, 'Dataset/CreditApproval/crx.data', 'Dataset/CreditApproval/crx.attr', 0, '+'],
        ['Letter Recognition', 20000, 'Dataset/LetterRecognition/letter-recognition.data', 'Dataset/LetterRecognition/letter-recognition.attr', 1, 'U'],
        ['Spam Base', 4601, 'Dataset/SpamBase/spambase.data', 'Dataset/SpamBase/spambase.attr', 1, '1'],
        ['Chess', 28056, 'Dataset/Chess/krkopt.data', 'Dataset/Chess/krkopt.attr', 0, 'fourteen'],
        ['Census Income', 32561, 'Dataset/Adult/adult.data', 'Dataset/Adult/adult-attr.txt', 0, '>50K']
    ]
    threshold = int(input('Enter pruning threshold(0 means \'without pruning\'): '))
    num_of_folds = 10
    print(len(dataset))
    for i in range(0, len(dataset)):
        print('_________________________________')
        print('Dataset Name:', dataset[i][0], '| Positive Class: ', dataset[i][5])
        CV().cross_validation(num_of_folds, dataset[i][0], dataset[i][1], dataset[i][2], dataset[i][3], dataset[i][4],
                              dataset[i][5], threshold)





