import pandas as pd
import numpy as np

from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from data_transform import handmark_transform

idxes = [5000*(i+1) for i in range(2)]
feature_files = [f'../data/training/new_features_{idx}.csv' for idx in idxes]
label_files = [f'../data/training/new_labels_{idx}.csv' for idx in idxes]

df = pd.DataFrame()
for feature_file, label_file in zip(feature_files, label_files):
    feat_df = pd.read_csv(feature_file, index_col=0)
    label_df = pd.read_csv(label_file, index_col=0)
    feat_df['label'] = label_df['0']

    df = pd.concat([df, feat_df])

## classifier
y = df['label'].to_numpy()
X = df.drop(columns=["label"]).to_numpy()

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y,random_state=1)
clf = MLPClassifier(random_state=1, max_iter=300).fit(X_train, y_train)
acc = clf.score(X_test, y_test)
print(acc)

unique, counts = np.unique(y, return_counts=True)

samples =[('../data/a/a2.jpg', 0), ('../data/a/a1.jpg', 0), ('../data/a/a3.jpg', 0), \
    ('../data/ethan_asl_2/B/WIN_20220210_00_43_39_Pro.jpg', 1), ('../data/ethan_asl_2/B/WIN_20220210_00_43_40_Pro.jpg', 1), \
     ('../data/ethan_asl_2/C/WIN_20220210_00_43_55_Pro.jpg', 2), ('../data/ethan_asl_2/C/WIN_20220210_00_43_58_Pro.jpg', 2), \
      ('../data/ethan_asl_2/a_test/a1.png', 0), ('../data/ethan_asl_2/a_test/a2.png', 0), ('../data/ethan_asl_2/a_test/d1.png', 3)]
feats, labels = handmark_transform(samples)
pred = clf.predict(feats)
print(pred)
print(labels)
