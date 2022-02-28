import glob
import os
import random
import numpy as np

allowed_labels = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "-", "_"]

# load hand gest dataset
def load_hand_gestures():
    hand_gest1 = glob.glob('..\data\hand_gestures_dataset\handgesturedataset_part1\*.png')
    hand_gest2 = glob.glob('..\data\hand_gestures_dataset\handgesturedataset_part2\*.png')
    hand_gest3 = glob.glob('..\data\hand_gestures_dataset\handgesturedataset_part3\*.png')
    hand_gest4 = glob.glob('..\data\hand_gestures_dataset\handgesturedataset_part4\*.png')
    hand_gest5 = glob.glob('..\data\hand_gestures_dataset\handgesturedataset_part5\*.png')

    hand_gests = [hand_gest1, hand_gest2, hand_gest3, hand_gest4, hand_gest5]

    image_paths = []
    labels = []
    for hand_gest in hand_gests:
        for filename in hand_gest:
            name = os.path.basename(filename)
            label = name[6].lower() # char at 6th is the label
            if label in allowed_labels:
                labels.append(label)
                image_paths.append(filename)

    return image_paths, labels

def image_folder_loader(rootdir, samples_per_letter = int(10e9)):
    image_paths = []
    labels = []

    for subdir, _, files in os.walk(rootdir):
        label = subdir[-1].lower() # char at -1 is the label
        # loops only over letters
        if label in allowed_labels:
            num_samples = min([samples_per_letter, len(files)])
            # sample some of the input files 
            files_included = random.sample(files, num_samples)
            for file in files_included:
                labels.append(label)
                image_paths.append(os.path.join(subdir, file))

    return image_paths, labels

def load_alphabet_test():
    rootdir = '../data/asl_alphabet_test_dataset/'
    image_paths, labels = image_folder_loader(rootdir, samples_per_letter=300)
    return image_paths, labels

def load_ethan_asl():
    rootdir = '../data/ethan_asl_3_dataset/'
    image_paths, labels = image_folder_loader(rootdir)
    return image_paths, labels

def load_alphabet():
    rootdir = '../data/asl_alphabet_dataset/'
    image_paths, labels = image_folder_loader(rootdir, samples_per_letter=300)
    return image_paths, labels

def load_fingerspelling():
    rootdir = '../data/fingerspelling_dataset/'
    image_paths, labels = image_folder_loader(rootdir, samples_per_letter=120)
    return image_paths, labels

def load_all():
    image_paths_hg, labels_hg = load_hand_gestures()
    image_paths_at, labels_at = load_alphabet_test()
    image_paths_a, labels_a = load_alphabet()
    image_paths_fs, labels_fs = load_fingerspelling()

    image_paths = image_paths_hg + image_paths_at + image_paths_a + image_paths_fs
    labels = labels_hg + labels_at + labels_a + labels_fs

    return image_paths, labels


if __name__ == "__main__":
    paths, labels = load_alphabet()
    print(paths[-3:])
    print(np.unique(labels))

    #paths, labels = load_all()
    #print(paths[:3])
    #print(labels[:3])



