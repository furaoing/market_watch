import pynlpir
import os
import math


def folder_parser(folder_path):
    file_names = os.listdir(folder_path)
    dirname = folder_path
    files = list()
    for file_name in file_names:
        files.append(os.path.join(dirname, file_name))
    return files


class TfParser(object):
    def __init__(self, file):
        with open(file, 'r', encoding="utf-8") as f:
            content = f.read()
            pynlpir.open()
            result = pynlpir.segment(content, pos_tagging=False)
        self.PoS = result

    def __call__(self):
        vector_space = set(self.PoS)
        tf_vector = {element: 0 for element in vector_space}
        for pos in self.PoS:
            if pos in vector_space:
                tf_vector[pos] += 1
        return vector_space, tf_vector


class BatchProcessor(object):
    def __init__(self, folder_path):
        tf_vector = list()
        global_pos = set()
        N = len(os.listdir(folder_path))
        files = folder_parser(folder_path)
        for file in files:
            parser = TfParser(file)   #construct a parser
            pos_buffer, vector_buffer = parser()
            tf_vector.append(vector_buffer)
            global_pos = global_pos | pos_buffer
        self.global_pos = global_pos
        self.df = None
        self.tf_vector = tf_vector
        self.N = N

    def idf(self):
        global_pos_list = {pos : 0 for pos in self.global_pos}
        for vector in self.tf_vector:
            intersection = set(vector.keys()) & self.global_pos
            for element in intersection:
                global_pos_list[element] += 1

        self.df = global_pos_list

        for key in global_pos_list.keys():
            global_pos_list[key] = math.log(self.N/global_pos_list[key], 10)
            # TODO: global_pos_list[key] might equals zero
        return global_pos_list

    def tfidf(self):
        idf = self.idf()
        for vector in self.tf_vector:
            for key in vector.keys():
                vector[key] *= idf[key]
        return self.tf_vector     #transmform tf vector into tfidf vector


class feature_selection(object):
    def __init__(self, mode, max_feature):
        self.mode = mode
        self.max_feature = max_feature

    def df_rank(self, df):
        df_ranked_list = sorted(df.items(), key = lambda d:d[1])
        return df_ranked_list

    def select(self, df):
        df_list = self.df_rank(df)
        compare = [self.max_feature, len(df_list)]
        feature_shape = min(compare)
        feature = list()
        for i in range(feature_shape):
            feature.append(df_list[i][0])
        return feature

folder_path = r'C:\workspace\训练数据\SVM训练测试\corpos\training_set\有效'
bp = BatchProcessor(folder_path)
tf_idf = bp.tfidf()

print(bp.df)
"""
selector = feature_selection(1, 200)

feature = selector.select(bp.df)

print(feature)
"""

