# -*- coding: utf-8 -*-

from baseClass import TfParser


def tf_vec_normalization(vec, norm="l1_norm"):
    if norm == "l1_norm":
        sumation = sum(vec)
        new_vec = [ele/sumation for ele in vec]
    else:
        print("Wrong Argument Provided !")
        raise BaseException
    return new_vec


def cosine(vector_a, vector_b):
    def l2_norm(vector):
        norm_squared = 0
        for ele in vector:
            norm_squared += ele**2
        norm = norm_squared**0.5
        return norm

    l2_norm_a = l2_norm(vector_a)
    l2_norm_b = l2_norm(vector_b)
    dot_product = sum([vector_a[i]*vector_b[i] for i in range(len(vector_a))])
    cosine = dot_product/(l2_norm_a*l2_norm_b)
    return cosine


def tf_vector(content):
    parser = TfParser(content)
    return parser()[0], parser()[1]


def cal_similarity(file_a, file_b):
    vector_space_a, tf_a = tf_vector(file_a)
    vector_space_b, tf_b = tf_vector(file_b)
    vector_space = vector_space_a | vector_space_b
    vector_ele_pos_mapping = list(vector_space)
    vector_a = [0 for ele in range(len(vector_ele_pos_mapping))]
    vector_b = list(vector_a)
    for key in tf_a.keys():
        position = vector_ele_pos_mapping.index(key)
        vector_a[position] = tf_a[key]
    for key in tf_b.keys():
        position = vector_ele_pos_mapping.index(key)
        vector_b[position] = tf_b[key]
    cos = cosine(vector_a, vector_b)
    return cos

if __name__ == "__main__":
    file_path = [r"test_cosine/0", r"test_cosine/1"]
    cal_similarity(file_path[0], file_path[1])
