import numpy as np
import matplotlib.pyplot as plt
from joblib import dump, load

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

import preprocess.dataset_loaders as dl

print("Loading train data...")
X = np.load('output/train_features.npy')
y = np.load('output/train_labels.npy')

print("Loading test data...")
X_test = np.load('output/test_features.npy')
y_test = np.load('output/test_labels.npy')

X_train, X_val, y_train, y_val = train_test_split(X, y, stratify=y, random_state=1)

print("Training classifier...")

clf = MLPClassifier(random_state=1, max_iter=300).fit(X_train, y_train)

train_accuracy = clf.score(X_train, y_train)
print(f"Train Accuracy: {train_accuracy}")

val_accuracy = clf.score(X_val, y_val)
print(f"Val Accuracy: {val_accuracy}")

test_accuracy = clf.score(X_test, y_test)
print(f"Test Accuracy: {test_accuracy}")

y_pred = clf.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
cm_display = ConfusionMatrixDisplay(cm, display_labels=dl.allowed_labels).plot()
plt.show()

dump(clf, "output/model.joblib")
