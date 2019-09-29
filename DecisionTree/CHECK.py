from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.tree.export import export_text
import matplotlib.pyplot as plt

iris = load_iris()
clf = tree.DecisionTreeClassifier(criterion="entropy")
clf = clf.fit(iris.data, iris.target)
print(iris.data)
print(iris.target)
tree.plot_tree(clf.fit(iris.data, iris.target))

plt.show()
r = export_text(clf, feature_names=iris['feature_names'])
print(r)