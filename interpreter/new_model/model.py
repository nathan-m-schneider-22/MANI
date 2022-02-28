import numpy as np
import matplotlib.pyplot as plt
import wandb
from joblib import dump, load

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier

from scipy.stats import zscore

import preprocess.dataset_loaders as dl

## model parameters
model_name = "MLP"
feature_names = ["distance", "segment_angles", "axis_angles"]
feature_idxes = [np.arange(0, 210), np.arange(210, 651), np.arange(651, 714)]
feature_names = [feature_names[1], feature_names[2]]
feature_idxes = [feature_idxes[1], feature_idxes[2]]

base_path = "output/distance_segment_angles/"
plot_cm = False
log = True
normalize = False
augment = False
ensemble = True
n_ensemble_iters = 15

## logger
if log:
    config = {
        "model_name": model_name,
        "feature_names": feature_names
    }
    wandb.init(project="asl-mp", entity="et22", config = config)
    wb_name = model_name + ", features: " + str(feature_names)
    if normalize:
        wb_name = wb_name + " normalized"
    if ensemble:
        wb_name = wb_name + f" ensemble: {n_ensemble_iters} iters"
    wandb.run.name = wb_name

## training
print("Loading train data...")
X = np.load(f'{base_path}/train_features.npy')
y = np.load(f'{base_path}/train_labels.npy')

print("Loading test data...")
X_test = np.load(f'{base_path}/test_features.npy')
y_test = np.load(f'{base_path}/test_labels.npy')

X_n = np.empty(shape=(X.shape[0],0))
X_tn = np.empty(shape=(X_test.shape[0],0))
for idxes in feature_idxes:
    X_n = np.hstack((X_n, X[:, idxes]))
    X_tn = np.hstack((X_tn, X_test[:, idxes]))

X = X_n
X_test = X_tn

X_train, X_val, y_train, y_val = train_test_split(X, y, stratify=y, random_state=1)

print("Training classifier...")   

if normalize:
    mu = np.mean(X_train, 0)
    sigma = np.std(X_train, 0)
    X_train = (X_train-mu)/sigma
    X_val = (X_val-mu)/sigma
    X_test = (X_test-mu)/sigma

if augment:
    sigma = np.std(X_train, 0)
    num_rows = X_train.shape[0]
    sigma_tile = np.tile(sigma, [num_rows, 1])
    xtrain_list = [X_train]
    ytrain_list = [y_train]
    np.random.seed(1)
    for i in range(2):
        add_to_train = (np.random.randn(*sigma_tile.shape))*sigma_tile
        xtrain_list.append(X_train+add_to_train)
        ytrain_list.append(y_train)
    X_train = np.vstack(xtrain_list)
    y_train = np.concatenate(ytrain_list)

if ensemble:
    iters = n_ensemble_iters
else:
    iters = 1

clfs = []

for i in range(iters):
    if model_name == 'MLP':
        clf = MLPClassifier(random_state=i+1, max_iter=300)
    elif model_name == 'SVM':
        clf = SVC(gamma=2, C=1, probability=True)
    elif model_name == 'Decision Tree':
        clf = DecisionTreeClassifier(max_depth=10)
    elif model_name == 'Random Forest':
        clf = RandomForestClassifier(max_depth=10, n_estimators=10, max_features=1)
    elif model_name == 'KNN':
        clf = KNeighborsClassifier(5)
    else:
        raise ValueError(f"Invalid model name {model_name}")
    
    clfs.append((f'clf_{i}', clf))

if ensemble:
    clf = VotingClassifier(estimators=clfs, voting='soft')

# fit the model
clf.fit(X_train, y_train)

# compute accuracy
train_accuracy = clf.score(X_train, y_train)
print(f"Train Accuracy: {train_accuracy}")

val_accuracy = clf.score(X_val, y_val)
print(f"Val Accuracy: {val_accuracy}")

test_accuracy = clf.score(X_test, y_test)
print(f"Test Accuracy: {test_accuracy}")

y_pred = clf.predict(X_test)
y_probas = clf.predict_proba(X_test)
labels = dl.allowed_labels

if log:
    # logging train, val and test accuracy 
    labels = ["Train Accuracy", "Val Accuracy", "Test Accuracy"]
    values = [train_accuracy, val_accuracy, test_accuracy]
    data = [[label, val] for (label, val) in zip(labels, values)]
    table = wandb.Table(data=data, columns = ["Dataset", "Accuracy"])
    wandb.log({"Accuracy" : wandb.plot.bar(table, "Dataset", "Accuracy",
                                title="Accuracy")})

    # logging confusion matrix
    preds = np.argmax(y_probas, axis=1)
    dl.allowed_labels.sort()
    y_test = np.array([dl.allowed_labels.index(y) for y in y_test])
    wandb.log({"Confusion Matrix" : wandb.plot.confusion_matrix(probs=None,
                            y_true=y_test, preds=preds,
                            class_names=dl.allowed_labels)})

dump(clf, "output/model.joblib")
