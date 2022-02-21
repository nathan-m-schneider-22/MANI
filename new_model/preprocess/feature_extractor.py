import mediapipe as mp
import cv2
import numpy as np
import numpy.linalg as la
import scipy
from scipy.spatial.distance import pdist
from scipy.stats import zscore
from os.path import exists


from preprocess.dataset_loaders import load_all, load_ethan_asl, load_alphabet, load_hand_gestures, load_alphabet_test
from preprocess.dataset_loaders import load_fingerspelling

def images_to_landmarks(paths, labels, mode='inference'):
    if mode == 'debug':
        print("Convering images to landmarks...")

    num_images = len(paths)
    mp_hands = mp.solutions.hands

    landmarks = []
    landmark_labels = []

    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=.2) as hands:
        for idx, (file, label) in enumerate(zip(paths, labels)):
            image = cv2.flip(cv2.imread(file), 1)
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if mode == 'debug':
                if idx % 250 == 0:
                    print(f"Progress:{idx}/{num_images}")

            if not results.multi_hand_landmarks:
                continue

            for hand_landmarks in results.multi_hand_landmarks:
                landmarks.append(hand_landmarks)
                landmark_labels.append(label)
                break

    if mode == 'debug':
        print("Finished conversion!")

    return landmarks, landmark_labels


def extract_distances(landmarks_list):
    distance_features = []
    for landmarks in landmarks_list:
        dists = pdist(landmarks)
        dists = zscore(dists)
        distance_features.append(dists)                    
    
    return np.array(distance_features)

def extract_pairwise_angles(landmarks_list):
    angle_features = []
    for landmarks in landmarks_list:
        x = landmarks
        y = landmarks

        dotprod_mat = np.einsum('ij,kj->ik', x, y)
        costheta = dotprod_mat / la.norm(x, axis=1)[:, np.newaxis]
        costheta /= la.norm(y, axis=1)
        angles = costheta.flatten()
        angles = np.nan_to_num(angles)
        angle_features.append(angles)
    
    return np.array(angle_features)

def extract_axis_angles(landmarks_list):
    angle_features = []
    for landmarks in landmarks_list:
        x = landmarks
        y = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

        dotprod_mat = np.einsum('ij,kj->ik', x, y)
        costheta = dotprod_mat / la.norm(x, axis=1)[:, np.newaxis]
        costheta /= la.norm(y, axis=1)
        angles = costheta.flatten()
        angles = np.nan_to_num(angles)
        angle_features.append(angles)
    
    return np.array(angle_features)

def landmarks_to_np(landmarks_list, mode = 'inference'):
    if mode == 'debug':
        print("Convering landmarks to numpy array...")

    landmarks_list_np = []
    for landmarks in landmarks_list:
        landmarks_np = np.ones((21, 3))
        for idx, lm in enumerate(landmarks.landmark):
            landmarks_np[idx,:] = [lm.x, lm.y, lm.z]
        landmarks_list_np.append(landmarks_np)

    if mode == 'debug':
        print("Finished conversion!")

    return landmarks_list_np


def extract_features(paths, labels, input_type='images'):
    if input_type == 'images':
        landmarks_list, landmarks_labels = images_to_landmarks(paths, labels)
    elif input_type == 'inference':
        landmarks_list = paths
        landmarks_labels = labels

    # transform labels
    labels = np.array(landmarks_labels)

    # transform features
    landmarks_np = landmarks_to_np(landmarks_list)
    distance_features = extract_distances(landmarks_np)
    pairwise_angle_features = extract_pairwise_angles(landmarks_np)
    axis_angle_features = extract_axis_angles(landmarks_np)

    features = np.hstack([distance_features, pairwise_angle_features, axis_angle_features])

    return features, labels

def extract_dataset(dataset_name):
    feature_output_file = f'../output/{dataset_name}_features.npy'
    label_output_file =  f'../output/{dataset_name}_labels.npy'

    if exists(feature_output_file) and exists(label_output_file):
        features = np.load(feature_output_file)
        labels = np.load(label_output_file)
    else:
        if dataset_name == "hand_gestures":
            paths, labels = load_hand_gestures()
        elif dataset_name == "alphabet":
            paths, labels = load_alphabet()
        elif dataset_name == "fingerspelling":
            paths, labels = load_fingerspelling()
        elif dataset_name == "alphabet_test":
            paths, labels = load_alphabet_test()
        elif dataset_name == "ethan_asl":
            paths, labels = load_ethan_asl()
        else:
            raise ValueError("Invalid dataset name")
        
        features, labels = extract_features(paths, labels)

        np.save(feature_output_file, features)
        np.save(label_output_file, labels)

    return features, labels

if __name__ == "__main__":
    test_features = np.array([])
    test_labels = np.array([])
    test_dataset_list = ["ethan_asl"]
    for dataset in test_dataset_list:
        features, labels = extract_dataset(dataset)
        test_features = np.vstack([test_features, features]) if test_features.size else features
        test_labels = np.concatenate([test_labels, labels]) if test_labels.size else labels
    

    np.save('../output/test_features.npy', test_features)
    np.save('../output/test_labels.npy', test_labels)

    train_features = np.array([])
    train_labels = np.array([])
    train_dataset_list = ["hand_gestures", "alphabet_test", "alphabet", "fingerspelling"]
    for dataset in train_dataset_list:
        features, labels = extract_dataset(dataset)
        train_features = np.vstack([train_features, features]) if train_features.size else features
        train_labels = np.concatenate([train_labels, labels]) if train_labels.size else labels
    
    np.save('../output/train_features.npy', train_features)
    np.save('../output/train_labels.npy', train_labels)

