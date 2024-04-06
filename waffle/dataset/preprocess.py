# -*- coding: utf-8 -*-

import random
import os
import shutil


def dataset_split(dataset, ratio):
    # split raw dataset into a training/verification pair based on a ratio

    def pro_type_a(_dataset, _ratio):
        n_samples = len(_dataset)
        n_training_samples = int(n_samples * _ratio)

        random.shuffle(_dataset)
        _training_samples = _dataset[:n_training_samples]
        _verification_samples = _dataset[n_training_samples:]
        return _training_samples, _verification_samples

    training_samples = None
    verification_samples = None

    if not 0 < ratio < 1:
        print("Ratio must be a position number larger than 1")
        raise Exception

    if type(dataset) == list:
        if type(dataset[0]) == str:
            training_samples, verification_samples = pro_type_a(dataset, ratio)

    return training_samples, verification_samples


def split_in_half():
    folder_path = r'corpos\排除（抽样）'

    files = os.listdir(folder_path)

    random.shuffle(files)

    samples = files[0:3000]

    new_folder_path = r'corpos\training_set\排除'

    if not os.path.isdir(new_folder_path):
        os.mkdir(new_folder_path)

    for sample in samples:
        shutil.copyfile(folder_path + '\\' + sample, new_folder_path + '\\' + sample)

    samples = files[3000:6000]

    new_folder_path = r'corpos\verification_set\排除'

    if not os.path.isdir(new_folder_path):
        os.mkdir(new_folder_path)

    for sample in samples:
        shutil.copyfile(folder_path + '\\' + sample, new_folder_path + '\\' + sample)