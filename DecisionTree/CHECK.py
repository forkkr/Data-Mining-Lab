# from sklearn.datasets import load_iris
# from sklearn import tree
# from sklearn.tree.export import export_text
# import matplotlib.pyplot as plt
#
# iris = load_iris()
# clf = tree.DecisionTreeClassifier(criterion="entropy")
# clf = clf.fit(iris.txt, iris.target)
# print(iris.txt)
# print(iris.target)
# tree.plot_tree(clf.fit(iris.txt, iris.target))
#
# plt.show()
# r = export_text(clf, feature_names=iris['feature_names'])
# print(r)
file = open('Dataset/WineQuality/winequality-white.csv', 'r')
wfile = open('Dataset/WineQuality/winequality.data', 'w')
for tp in file:
    tp = tp.replace(';', ',')
    print(tp)
    wfile.write(tp)
wfile.close()
file.close()