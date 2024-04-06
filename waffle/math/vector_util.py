# -*- coding: utf-8 -*-

import numpy as np
import logging


def l1_norm(vector):
    """
    Calcute the l1 norm of the vector given
    No Matrix Computation, no need to use np-array
    """
    my_sum = 0
    for ele in vector:
        if not ele:
            logging.warning("None-Type element found, computation was forced to stop")
            raise Exception
        my_sum += abs(ele)
    norm = my_sum/len(vector)
    return norm


def l2_norm(vector):
    """
    Calcute the l2 norm of the vector given (Euclidean Norm)
    """
    norm_squared = 0
    for ele in vector:
        if not ele:
            logging.warning("None-Type element found, computation was forced to stop")
            raise Exception
        norm_squared += ele**2
    norm = norm_squared**0.5
    return norm


def dot_product(vector_a, vector_b):
    """
    :param vector_a:  List
    :param vector_b:  List
    :return: normal_vec: List
    """
    np_vec_a = np.array(vector_a)
    np_vec_b = np.array(vector_b)
    dot_proc = np.dot(np_vec_a, np_vec_b)
    normal_vec = dot_proc.tolist()
    return normal_vec


def cosine(vector_a, vector_b):
    """
    :param vector_a:
    :param vector_b:
    :return:
    """

    l2_norm_a = l2_norm(vector_a)
    l2_norm_b = l2_norm(vector_b)

    d_proc = dot_product(vector_a, vector_b)
    my_cosine = d_proc/(l2_norm_a*l2_norm_b)
    return my_cosine


if __name__ == "__main__":
    v_a = [1, 2]
    v_b = [1, 2111]

    print(cosine(v_a, v_b))
