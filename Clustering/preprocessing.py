
# class Preprocess():
#
#     def __init__(self):
#         pass
#
#     # R15, glass, iris, seeds, thyroid
#
#


if __name__ == '__main__':

    file = open('../Clustering/dataset/aggregation/Aggregation.txt', 'r')
    dt_file = open('../Clustering/dataset/aggregation/Aggregation.data', 'w')
    cls_file = open('../Clustering/dataset/aggregation/Aggregation.class', 'w')

    for tup in file:
        lst = tup.split('\t')
        print(lst[-1])
        cls_file.write(lst[-1])
        # cls_file.write('\n')
        lst = lst[:len(lst)-1]
        print(lst)
        print(','.join(lst))
        dt_file.write(','.join(lst))
        dt_file.write('\n')
    dt_file.close()
    cls_file.close()
